import re
from urllib.parse import urlparse

class ProfileValidator:
    @staticmethod
    def validate_linkedin_url(url):
        """
        Validates all LinkedIn profile URL formats
        Returns: (is_valid, normalized_url)
        """
        if not url or not isinstance(url, str):
            return False, None
            
        url = url.strip()
        
        # Pattern 1: Full URL (with or without protocol)
        full_url_pattern = r'^(https?:\/\/)?(www\.)?linkedin\.com\/in\/([a-zA-Z0-9-]+)\/?$'
        
        # Pattern 2: Just the username
        username_pattern = r'^[a-zA-Z0-9-]+$'
        
        match = re.match(full_url_pattern, url)
        if match:
            username = match.group(3)
            return True, f"https://www.linkedin.com/in/{username}"
        
        if re.match(username_pattern, url):
            return True, f"https://www.linkedin.com/in/{url}"
        
        return False, None