import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import logging
from typing import List, Dict, Optional, Tuple
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from apscheduler.schedulers.blocking import BlockingScheduler
from sklearn.linear_model import LinearRegression
import io
import tempfile
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('reporting_pipeline.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Comprehensive data cleaning pipeline
    """
    logger.info(f"Starting data cleaning on {len(df)} rows")
    
    # Create a copy to avoid modifying original
    df_cleaned = df.copy()
    
    # Remove duplicates
    df_cleaned = df_cleaned.drop_duplicates()
    
    # Handle missing values
    numeric_columns = df_cleaned.select_dtypes(include=[np.number]).columns
    categorical_columns = df_cleaned.select_dtypes(include=['object']).columns
    
    # Fill numeric missing values with median
    for col in numeric_columns:
        df_cleaned[col] = df_cleaned[col].fillna(df_cleaned[col].median())
    
    # Fill categorical missing values with mode
    for col in categorical_columns:
        df_cleaned[col] = df_cleaned[col].fillna(df_cleaned[col].mode()[0])
    
    # Remove outliers using IQR method for numeric columns
    for col in numeric_columns:
        Q1 = df_cleaned[col].quantile(0.25)
        Q3 = df_cleaned[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        df_cleaned = df_cleaned[(df_cleaned[col] >= lower_bound) & (df_cleaned[col] <= upper_bound)]
    
    logger.info(f"Data cleaning complete. {len(df_cleaned)} rows retained.")
    return df_cleaned


def run_forecasts(df: pd.DataFrame) -> Dict[str, np.ndarray]:
    """
    Generate forecasts using multiple methods
    """
    logger.info("Starting forecast generation")
    
    forecasts = {}
    
    # Ensure we have a date column for time series
    date_col = None
    for col in df.columns:
        if 'date' in col.lower() or df[col].dtype == 'datetime64[ns]':
            date_col = col
            break
    
    if date_col:
        df = df.sort_values(by=date_col)
        df['date_ordinal'] = pd.to_datetime(df[date_col]).map(datetime.toordinal)
        
        # Forecast for each numeric column
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        if 'date_ordinal' in numeric_cols:
            numeric_cols.remove('date_ordinal')
        
        for col in numeric_cols[:3]:  # Limit to first 3 numeric columns
            try:
                X = df['date_ordinal'].values.reshape(-1, 1)
                y = df[col].values
                
                model = LinearRegression()
                model.fit(X, y)
                
                # Forecast next 30 days
                last_date = df['date_ordinal'].max()
                future_dates = np.arange(last_date + 1, last_date + 31).reshape(-1, 1)
                predictions = model.predict(future_dates)
                
                forecasts[col] = predictions
                logger.info(f"Forecast generated for {col}")
            except Exception as e:
                logger.error(f"Failed to forecast {col}: {e}")
    
    return forecasts


def generate_pdf_report(df: pd.DataFrame, forecasts: Dict, output_path: str) -> str:
    """
    Generate comprehensive PDF report with visualizations
    """
    logger.info("Starting PDF report generation")
    
    try:
        # Create figure with subplots
        fig = plt.figure(figsize=(16, 12))
        
        # Data summary
        ax1 = plt.subplot(2, 2, 1)
        df.select_dtypes(include=[np.number]).describe().loc['mean'].plot(kind='bar', ax=ax1)
        ax1.set_title('Average Metrics Summary')
        ax1.set_ylabel('Mean Value')
        plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45)
        
        # Trend analysis
        ax2 = plt.subplot(2, 2, 2)
        date_col = None
        for col in df.columns:
            if 'date' in col.lower() or df[col].dtype == 'datetime64[ns]':
                date_col = col
                break
        
        if date_col:
            numeric_col = df.select_dtypes(include=[np.number]).columns[0]
            df.groupby(df[date_col].dt.to_period('M'))[numeric_col].mean().plot(ax=ax2)
            ax2.set_title(f'Monthly Trend: {numeric_col}')
            ax2.set_xlabel('Date')
            ax2.set_ylabel('Average')
        
        # Forecast visualization
        ax3 = plt.subplot(2, 2, 3)
        if forecasts:
            for col, preds in list(forecasts.items())[:1]:  # Plot first forecast
                ax3.plot(preds, label=f'{col} Forecast', marker='o')
                ax3.set_title('30-Day Forecast')
                ax3.set_xlabel('Days Ahead')
                ax3.set_ylabel('Predicted Value')
                ax3.legend()
        
        # Data distribution
        ax4 = plt.subplot(2, 2, 4)
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        if len(numeric_columns) > 0:
            df[numeric_columns[0]].hist(bins=30, ax=ax4)
            ax4.set_title(f'Distribution: {numeric_columns[0]}')
            ax4.set_xlabel('Value')
            ax4.set_ylabel('Frequency')
        
        plt.tight_layout()
        
        # Save to PDF
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            plt.savefig(tmp_file.name, format='pdf', dpi=300, bbox_inches='tight')
            plt.close()
            
            # Copy to final location
            import shutil
            shutil.copy(tmp_file.name, output_path)
            os.unlink(tmp_file.name)
        
        logger.info(f"PDF report successfully generated at {output_path}")
        return output_path
    
    except Exception as e:
        logger.error(f"Failed to generate PDF report: {e}")
        raise


def send_email_with_attachment(
    to_emails: List[str],
    subject: str,
    body: str,
    attachment_path: str,
    smtp_config: Dict
) -> bool:
    """
    Send email with PDF attachment
    """
    logger.info(f"Sending email to {len(to_emails)} recipients")
    
    try:
        msg = MIMEMultipart()
        msg['From'] = smtp_config['sender']
        msg['To'] = ', '.join(to_emails)
        msg['Subject'] = subject
        
        # Attach body
        msg.attach(MIMEText(body, 'plain'))
        
        # Attach PDF
        with open(attachment_path, 'rb') as f:
            pdf_attachment = MIMEApplication(f.read(), _subtype='pdf')
            pdf_attachment.add_header(
                'Content-Disposition',
                'attachment',
                filename=os.path.basename(attachment_path)
            )
            msg.attach(pdf_attachment)
        
        # Send email
        with smtplib.SMTP(smtp_config['host'], smtp_config['port']) as server:
            server.starttls()
            server.login(smtp_config['username'], smtp_config['password'])
            server.send_message(msg)
        
        logger.info("Email sent successfully")
        return True
    
    except Exception as e:
        logger.error(f"Failed to send email: {e}")
        return False


def automate_reporting_pipeline(
    df: pd.DataFrame, 
    email_list: List[str],
    smtp_config: Optional[Dict] = None,
    output_dir: str = './reports'
) -> str:
    """
    Complete automated reporting pipeline that cleans data, runs forecasts, 
    generates PDF, and emails stakeholders.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Raw input data
    email_list : List[str]
        List of stakeholder email addresses
    smtp_config : Dict, optional
        SMTP configuration with keys: host, port, username, password, sender
    output_dir : str
        Directory to save generated reports
    
    Returns:
    --------
    str
        Success message with recipient count
    """
    logger.info("="*60)
    logger.info("STARTING AUTOMATED REPORTING PIPELINE")
    logger.info(f"Timestamp: {datetime.now()}")
    logger.info(f"Input data shape: {df.shape}")
    logger.info(f"Recipients: {len(email_list)}")
    
    try:
        # Step 1: Clean data
        cleaned_df = clean_data(df)
        
        # Step 2: Run forecasts
        forecasts = run_forecasts(cleaned_df)
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Step 3: Generate PDF report
        report_date = datetime.now().strftime('%Y-%m-%d')
        report_path = os.path.join(output_dir, f'executive_report_{report_date}.pdf')
        generate_pdf_report(cleaned_df, forecasts, report_path)
        
        # Step 4: Send email if configured
        if smtp_config and email_list:
            subject = f"Weekly Executive Report - {report_date}"
            body = f"""
            Hello,
            
            Please find attached the weekly executive report generated on {datetime.now().strftime('%A, %B %d, %Y')}.
            
            Report Summary:
            - Data points processed: {len(cleaned_df):,}
            - Metrics analyzed: {len(cleaned_df.select_dtypes(include=[np.number]).columns)}
            - Forecasts generated: {len(forecasts)}
            
            Best regards,
            Automated Reporting System
            
            ---
            This is an automated message. Do not reply.
            """
            
            send_email_with_attachment(
                to_emails=email_list,
                subject=subject,
                body=body,
                attachment_path=report_path,
                smtp_config=smtp_config
            )
        
        logger.info("PIPELINE COMPLETED SUCCESSFULLY")
        logger.info("="*60)
        
        return f"Report delivered to {len(email_list)} stakeholders"
        
    except Exception as e:
        logger.error(f"CRITICAL PIPELINE FAILURE: {e}")
        logger.exception("Full traceback:")
        logger.info("="*60)
        raise


def schedule_weekly_report():
    """
    Scheduler that runs the pipeline every Monday at 6 AM
    """
    scheduler = BlockingScheduler()
    
    # Example job configuration
    def job():
        # Load your data here
        # df = pd.read_csv('your_data_source.csv')
        # email_list = ['exec@company.com', 'team@company.com']
        # smtp_config = {
        #     'host': 'smtp.company.com',
        #     'port': 587,
        #     'username': 'user@company.com',
        #     'password': 'your_password',
        #     'sender': 'reports@company.com'
        # }
        # 
        # automate_reporting_pipeline(df, email_list, smtp_config)
        pass
    
    scheduler.add_job(
        job,
        'cron',
        day_of_week='mon',
        hour=6,
        minute=0,
        timezone='America/New_York'
    )
    
    logger.info("Scheduler started. Next run: Monday 6:00 AM")
    scheduler.start()


# Usage Example:
if __name__ == "__main__":
    # Create sample data
    sample_data = pd.DataFrame({
        'date': pd.date_range('2024-01-01', periods=100),
        'revenue': np.random.normal(100000, 15000, 100),
        'users': np.random.randint(1000, 5000, 100),
        'churn_rate': np.random.uniform(0.02, 0.08, 100)
    })
    
    # Configuration
    EMAIL_LIST = ['ceo@company.com', 'cfo@company.com', 'cto@company.com']
    SMTP_CONFIG = {
        'host': 'smtp.gmail.com',
        'port': 587,
        'username': 'your_email@gmail.com',
        'password': 'your_app_password',
        'sender': 'your_email@gmail.com'
    }
    
    # Run pipeline
    result = automate_reporting_pipeline(
        df=sample_data,
        email_list=EMAIL_LIST,
        smtp_config=SMTP_CONFIG
    )
    print(result)
    
    # To schedule instead of immediate run:
    # schedule_weekly_report()
