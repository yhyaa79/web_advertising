
    document.addEventListener("DOMContentLoaded", function () {
        const navbar = document.getElementById('navbar');

        // یک تابع می‌سازیم که وضعیت نوار را بر اساس موقعیت اسکرول تنظیم کند
        function updateNavbar() {
            if (window.scrollY > 50) {
                // حالت اسکرول شده: نوار باید روشن باشد
                navbar.classList.add('navbar-scrolled');
                navbar.classList.remove('navbar-top');
            } else {
                // حالت بالای صفحه: نوار باید تیره باشد
                navbar.classList.add('navbar-top');
                navbar.classList.remove('navbar-scrolled');
            }
        }

        // ۱. بلافاصله بعد از لود شدن یا رفرش صفحه وضعیت را چک کن
        updateNavbar();

        // ۲. هنگام اسکرول کردن هم وضعیت را آپدیت کن
        window.addEventListener('scroll', updateNavbar);
    });
