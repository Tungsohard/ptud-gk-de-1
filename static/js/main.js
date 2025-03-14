// Xử lý sự kiện khi tài liệu HTML đã được tải hoàn toàn
document.addEventListener('DOMContentLoaded', function() {
    // Xử lý đóng thông báo flash
    const closeAlerts = document.querySelectorAll('.close-alert');
    closeAlerts.forEach(function(button) {
        button.addEventListener('click', function() {
            const alert = this.parentElement;
            alert.style.opacity = '0';
            setTimeout(function() {
                alert.style.display = 'none';
            }, 300);
        });
    });

    // Tự động ẩn thông báo flash sau 5 giây
    const alerts = document.querySelectorAll('.alert');
    if (alerts.length > 0) {
        setTimeout(function() {
            alerts.forEach(function(alert) {
                alert.style.opacity = '0';
                setTimeout(function() {
                    alert.style.display = 'none';
                }, 300);
            });
        }, 5000);
    }

    // Nếu trang có form, thêm sự kiện kiểm tra form
    const forms = document.querySelectorAll('form');
    forms.forEach(function(form) {
        form.addEventListener('submit', function(e) {
            // Kiểm tra các trường bắt buộc
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;
            
            requiredFields.forEach(function(field) {
                if (!field.value.trim()) {
                    isValid = false;
                    // Thêm class lỗi nếu cần
                    field.classList.add('is-invalid');
                } else {
                    field.classList.remove('is-invalid');
                }
            });

            if (!isValid) {
                e.preventDefault();
                const errorMessage = document.createElement('div');
                errorMessage.className = 'alert alert-danger';
                errorMessage.textContent = 'Vui lòng điền đầy đủ thông tin.';
                form.prepend(errorMessage);
                
                setTimeout(function() {
                    errorMessage.style.opacity = '0';
                    setTimeout(function() {
                        errorMessage.remove();
                    }, 300);
                }, 3000);
            }
        });
    });

    // Xử lý nút hamburger menu cho thiết bị di động
    const navToggle = document.querySelector('.nav-toggle');
    if (navToggle) {
        navToggle.addEventListener('click', function() {
            const nav = document.querySelector('nav ul');
            nav.classList.toggle('show');
        });
    }
});

// Xác nhận xóa bài viết hoặc tài khoản
function confirmDelete(message) {
    return confirm(message || 'Bạn có chắc chắn muốn xóa?');
}// This file is intentionally left blank.