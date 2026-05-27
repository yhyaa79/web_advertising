
/* ========================================
   سیستم نوتیفیکیشن
   ======================================== */

(function () {
    // ساخت container اگر وجود نداشت
    function getContainer() {
        let container = document.getElementById('notification-container');
        if (!container) {
            container = document.createElement('div');
            container.id = 'notification-container';
            document.body.appendChild(container);
        }
        return container;
    }

    const ICONS = {
        success: 'bi bi-check-circle-fill',
        info:    'bi bi-info-circle-fill',
        error:   'bi bi-x-circle-fill',
        warning: 'bi bi-exclamation-triangle-fill',
    };

    const DURATION = 4000; // میلی‌ثانیه

    /**
     * نمایش نوتیفیکیشن
     * @param {string} message - متن پیام
     * @param {'success'|'info'|'error'|'warning'} type - نوع الارم
     */
    window.showNotification = function (message, type = 'info') {
        if (!['success', 'info', 'error', 'warning'].includes(type)) {
            type = 'info';
        }

        const container = getContainer();

        const notif = document.createElement('div');
        notif.className = `notification ${type}`;
        notif.innerHTML = `
            <i class="notification-icon ${ICONS[type]}"></i>
            <span class="notification-text">${message}</span>
            <button class="notification-close" aria-label="بستن">&#x2715;</button>
            <div class="notification-progress" style="animation-duration: ${DURATION}ms;"></div>
        `;

        container.appendChild(notif);

        // بستن با دکمه
        notif.querySelector('.notification-close').addEventListener('click', () => {
            closeNotification(notif);
        });

        // بستن خودکار
        const timer = setTimeout(() => closeNotification(notif), DURATION);

        // نگه داشتن موس = توقف تایمر
        notif.addEventListener('mouseenter', () => {
            clearTimeout(timer);
            const progress = notif.querySelector('.notification-progress');
            if (progress) progress.style.animationPlayState = 'paused';
        });

        notif.addEventListener('mouseleave', () => {
            closeNotification(notif);
        });
    };

    function closeNotification(notif) {
        if (notif.classList.contains('hiding')) return;
        notif.classList.add('hiding');
        notif.addEventListener('animationend', () => notif.remove(), { once: true });
    }
})();







/* ========================================
   Modal Confirm
   ======================================== */

(function () {
    const ICONS = {
        warning: 'bi bi-exclamation-triangle-fill',
        error:   'bi bi-x-circle-fill',
        info:    'bi bi-info-circle-fill',
        success: 'bi bi-check-circle-fill',
    };

    /**
     * جایگزین confirm() مرورگر
     *
     * @param {Object} options
     * @param {string}   options.message              - متن سوال
     * @param {string}  [options.type='warning']      - نوع: warning | error | info | success
     * @param {string}  [options.confirmText='تأیید'] - متن دکمه تأیید
     * @param {string}  [options.cancelText='انصراف'] - متن دکمه انصراف
     * @returns {Promise<boolean>}
     *
     * @example
     * const ok = await showConfirm({ message: 'آیا مطمئنی؟' });
     * if (ok) { ... }
     */
    window.showConfirm = function ({
        message,
        type        = 'warning',
        confirmText = 'تأیید',
        cancelText  = 'انصراف',
    } = {}) {
        if (!['warning', 'error', 'info', 'success'].includes(type)) {
            type = 'warning';
        }

        return new Promise((resolve) => {
            // ساخت overlay
            const overlay = document.createElement('div');
            overlay.id = 'confirm-overlay';

            overlay.innerHTML = `
                <div id="confirm-box">
                    <div class="confirm-icon ${type}">
                        <i class="${ICONS[type]}"></i>
                    </div>
                    <div class="confirm-message">${message}</div>
                    <div class="confirm-actions">
                        <button class="confirm-btn confirm-btn-cancel">${cancelText}</button>
                        <button class="confirm-btn confirm-btn-ok ${type}">${confirmText}</button>
                    </div>
                </div>
            `;

            document.body.appendChild(overlay);

            // جلوگیری از اسکرول پس‌زمینه
            document.body.style.overflow = 'hidden';

            function close(result) {
                overlay.classList.add('hiding');
                overlay.addEventListener('animationend', () => {
                    overlay.remove();
                    document.body.style.overflow = '';
                    resolve(result);
                }, { once: true });
            }

            overlay.querySelector('.confirm-btn-ok').addEventListener('click', () => close(true));
            overlay.querySelector('.confirm-btn-cancel').addEventListener('click', () => close(false));

            // کلیک روی پس‌زمینه = انصراف
            overlay.addEventListener('click', (e) => {
                if (e.target === overlay) close(false);
            });

            // کلید Escape = انصراف
            function onKeydown(e) {
                if (e.key === 'Escape') {
                    document.removeEventListener('keydown', onKeydown);
                    close(false);
                }
                if (e.key === 'Enter') {
                    document.removeEventListener('keydown', onKeydown);
                    close(true);
                }
            }
            document.addEventListener('keydown', onKeydown);
        });
    };
})();
