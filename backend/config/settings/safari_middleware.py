class SafariSameSiteMiddleware:
    """
    Hotfix for Safari ITP / iOS WebKit SameSite=None bug.
    
    Safari < 12 and iOS WebKit incorrectly treat SameSite=None 
    as SameSite=Strict, blocking cross-origin cookies entirely.
    This middleware detects affected Safari versions and removes
    the SameSite=None attribute so cookies are sent normally.
    """
    
    AFFECTED_SAFARI = (
        'iPhone', 'iPad', 'Macintosh',
    )
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        
        if self._is_problematic_safari(user_agent):
            self._fix_samesite_cookies(response)
        
        return response

    def _is_problematic_safari(self, user_agent: str) -> bool:
        """
        Detects Safari browsers that mishandle SameSite=None.
        Chrome/Edge on iOS also uses WebKit but handles it correctly.
        """
        if 'Safari' not in user_agent:
            return False
        # Chrome and Edge on iOS/Mac are fine — they include 'Chrome' or 'EdgA'
        if 'Chrome' in user_agent or 'Chromium' in user_agent:
            return False
        if 'EdgA' in user_agent or 'Edge' in user_agent:
            return False
        # Remaining Safari (iOS Safari, macOS Safari) — apply fix
        return any(device in user_agent for device in self.AFFECTED_SAFARI)

    def _fix_samesite_cookies(self, response):
        """
        Remove SameSite=None from cookies for broken Safari versions.
        Falls back to SameSite=Lax which Safari handles correctly.
        """
        if not response.cookies:
            return
            
        for cookie in response.cookies.values():
            if cookie.get('samesite', '').lower() == 'none':
                cookie['samesite'] = 'Lax'