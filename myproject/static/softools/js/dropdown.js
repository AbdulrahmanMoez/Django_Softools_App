document.addEventListener('DOMContentLoaded', function() {
    const profileTrigger = document.querySelector('.profile-trigger');
    const profileDropdown = document.querySelector('.profile-dropdown');
    
    if (profileTrigger && profileDropdown) {
        // Toggle dropdown on trigger click
        profileTrigger.addEventListener('click', function(e) {
            e.stopPropagation();
            this.classList.toggle('active');
            profileDropdown.classList.toggle('active');
        });

        // Close dropdown when clicking outside
        document.addEventListener('click', function(e) {
            if (!profileDropdown.contains(e.target) && !profileTrigger.contains(e.target)) {
                profileTrigger.classList.remove('active');
                profileDropdown.classList.remove('active');
            }
        });

        // Close dropdown on escape key
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                profileTrigger.classList.remove('active');
                profileDropdown.classList.remove('active');
            }
        });
    }
}); 