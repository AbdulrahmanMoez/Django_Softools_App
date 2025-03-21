// Password visibility toggle
document.addEventListener('DOMContentLoaded', function() {
    const passwordFields = document.querySelectorAll('input[type="password"]');
    
    passwordFields.forEach(field => {
        // Create toggle button
        const toggle = document.createElement('span');
        toggle.innerHTML = '<i class="fas fa-eye"></i>';
        toggle.className = 'password-toggle';
        field.parentElement.style.position = 'relative';
        field.parentElement.appendChild(toggle);
        
        // Toggle password visibility
        toggle.addEventListener('click', () => {
            const type = field.getAttribute('type');
            field.setAttribute('type', type === 'password' ? 'text' : 'password');
            toggle.innerHTML = type === 'password' ? 
                '<i class="fas fa-eye-slash"></i>' : 
                '<i class="fas fa-eye"></i>';
        });
    });
    
    // Alert dismissal
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 300);
        }, 5000);
    });
});