from flask import Flask, render_template, request, redirect, url_for, flash, session
from core.scraper import LinkedInScraper
from core.exporter import DataExporter
from core.validator import ProfileValidator
import config
import os
import re
from datetime import datetime
from urllib.parse import urlparse

app = Flask(__name__)
app.secret_key = config.CONFIG['flask']['secret_key']
app.scraper = None

os.makedirs('Outputs', exist_ok=True)

def normalize_linkedin_url(input_url):
    """Normalize all LinkedIn URL formats"""
    if not input_url or not isinstance(input_url, str):
        return None
    url = input_url.strip().split('?')[0].split('#')[0]
    
    if url.startswith('https://www.linkedin.com/in/'):
        return url
    if url.startswith(('http://', 'https://', 'www.', 'linkedin.com/')):
        username = None
        if '/in/' in url:
            username = url.split('/in/')[-1].split('/')[0]
        elif url.startswith(('http://', 'https://')):
            username = urlparse(url).path.split('/')[-1]
        if username and re.match(r'^[a-zA-Z0-9-]+$', username):
            return f'https://www.linkedin.com/in/{username}'
    if re.match(r'^[a-zA-Z0-9-]+$', url):
        return f'https://www.linkedin.com/in/{url}'
    return None

@app.route('/', methods=['GET', 'POST'])
def index():
    popup_data = None
    if session.get('show_popup'):
        popup_data = {
            'message': session.pop('popup_message'),
            'type': session.pop('popup_type')
        }
        session.pop('show_popup')

    if request.method == 'POST':
        if 'login_auto' in request.form:  # Automatic login
            try:
                app.scraper = LinkedInScraper(headless=False)
                if app.scraper.login():
                    session['show_popup'] = True
                    session['popup_message'] = '✓ Login successful! Select scrape mode'
                    session['popup_type'] = 'success'
                else:
                    session['show_popup'] = True
                    session['popup_message'] = 'Login failed'
                    session['popup_type'] = 'error'
            except Exception as e:
                session['show_popup'] = True
                session['popup_message'] = f'Login failed: {str(e)}'
                session['popup_type'] = 'error'
                if app.scraper:
                    app.scraper.close()
                    app.scraper = None
            return redirect(url_for('index'))
        
        elif 'login_manual' in request.form:  # Manual login
            try:
                app.scraper = LinkedInScraper(headless=False)
                app.scraper.driver.get(config.CONFIG['linkedin']['login_url'])
                session['show_popup'] = True
                session['popup_message'] = 'Please complete login in the browser window, then return here'
                session['popup_type'] = 'info'
            except Exception as e:
                session['show_popup'] = True
                session['popup_message'] = f'Error: {str(e)}'
                session['popup_type'] = 'error'
            return redirect(url_for('index'))
        
        elif 'scrape_manual' in request.form:
            return handle_manual_scrape()
        
        elif 'scrape_auto' in request.form:
            return handle_auto_scrape()
    
    return render_template(
        'index.html',
        logged_in=app.scraper.is_logged_in() if app.scraper else False,
        popup=popup_data
    )

def handle_manual_scrape():
    if not app.scraper or not app.scraper.is_logged_in():
        flash('Please login first', 'error')
        return redirect(url_for('index'))
    
    profile_url = request.form.get('profile_url', '').strip()
    if not profile_url:
        flash('Please enter a profile URL', 'error')
        return redirect(url_for('index'))
    
    normalized_url = normalize_linkedin_url(profile_url)
    if not normalized_url:
        flash('Invalid LinkedIn URL format', 'error')
        return redirect(url_for('index'))
    
    try:
        profile_data = app.scraper.scrape_profile(normalized_url)
        if not profile_data:
            flash('Failed to scrape profile', 'warning')
            return redirect(url_for('index'))
        
        filename = generate_filename(profile_data)
        DataExporter.to_csv(profile_data, filename)
        # Add a session flag for successful scraping
        session['show_popup'] = True
        session['popup_message'] = f'✓ Manual scrape successful: {profile_data.get("name", "profile")}'
        session['popup_type'] = 'success'
    except Exception as e:
        flash(f'Manual scrape error: {str(e)}', 'error')
    
    return redirect(url_for('index'))

def handle_auto_scrape():
    if not app.scraper or not app.scraper.is_logged_in():
        flash('Please login first', 'error')
        return redirect(url_for('index'))
    
    input_file = request.files.get('profile_list')
    if not input_file or input_file.filename == '':
        flash('Please select a file for auto-scraping', 'error')
        return redirect(url_for('index'))
    
    try:
        content = input_file.read().decode('utf-8')
        urls = [line.strip() for line in content.splitlines() if line.strip()]
        
        if not urls:
            flash('File is empty', 'error')
            return redirect(url_for('index'))
        
        success_count = 0
        for url in urls:
            normalized_url = normalize_linkedin_url(url)
            if normalized_url:
                try:
                    profile_data = app.scraper.scrape_profile(normalized_url)
                    if profile_data:
                        filename = generate_filename(profile_data)
                        DataExporter.to_csv(profile_data, filename)
                        success_count += 1
                except:
                    continue
        
        # Add session flags for auto-scrape
        session['show_popup'] = True
        session['popup_message'] = f'✓ Auto-scrape completed: {success_count}/{len(urls)} profiles scraped'
        session['popup_type'] = 'success'
    except Exception as e:
        flash(f'Auto-scrape error: {str(e)}', 'error')
    
    return redirect(url_for('index'))

def generate_filename(profile_data):
    """Generate filename from profile data"""
    if profile_data.get('name'):
        clean_name = re.sub(r'[^\w-]', '_', profile_data['name'])
        return f"Outputs/{clean_name.strip('_').replace('__', '_')}.csv"
    return f"Outputs/profile_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

@app.route('/logout')
def logout():
    if app.scraper:
        app.scraper.close()
        app.scraper = None
    session['show_popup'] = True
    session['popup_message'] = '✓ Logged out successfully'
    session['popup_type'] = 'info'
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=config.CONFIG['flask']['debug'])