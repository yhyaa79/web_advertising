/*  ========================================
    باز و بسته کردن منوی گزینه های بیشتر در نوار اصلی

    templates/base.html 
   ========================================  */

document.addEventListener('DOMContentLoaded', function () {
    const dropBtn = document.getElementById('moreMenuBtn');
    const dropdown = document.getElementById('moreDropdown');

    // باز و بسته کردن منو با کلیک روی دکمه
    dropBtn.addEventListener('click', function (event) {
        event.preventDefault(); // جلوگیری از پرش صفحه به بالا
        dropdown.classList.toggle('show');
    });

    // بستن منو در صورت کلیک در هر جای دیگر از صفحه
    window.addEventListener('click', function (event) {
        if (!event.target.closest('.dropdown-container')) {
            if (dropdown.classList.contains('show')) {
                dropdown.classList.remove('show');
            }
        }
    });
});




/*  ========================================
    پرسش و پاسخ اگهی

    templates/listings/listing_detail.html
   ========================================  */

document.addEventListener('DOMContentLoaded', function () {
    // تغییر سلکتور به .faq-question تا با کلیک روی کل ردیف عمل کند
    document.querySelectorAll('.faq-question').forEach(function (row) {
        row.addEventListener('click', function () {
            const faqId = this.dataset.faqId;
            toggleFaq(faqId);
        });
    });

    function toggleFaq(faqId) {
        const wrapper = document.getElementById('faq-answer-wrapper-' + faqId);
        const answer = document.getElementById('faq-answer-' + faqId);
        // پیدا کردن آیکون و دکمه بر اساس ساختار جدید
        const parentRow = document.querySelector(`.faq-question[data-faq-id="${faqId}"]`);
        const icon = parentRow.querySelector('.faq-icon');
        const toggleBtn = parentRow.querySelector('.faq-toggle-btn');
        const questionBtn = parentRow.querySelector('.faq-question-div');

        const isOpen = wrapper.classList.contains('open');

        if (isOpen) {
            wrapper.style.maxHeight = '0';
            wrapper.classList.remove('open');
            if (icon) {
                icon.classList.remove('bi-chevron-up');
                icon.classList.add('bi-chevron-down');
            }
            if (toggleBtn) toggleBtn.classList.remove('open');
            if (questionBtn) questionBtn.setAttribute('aria-expanded', 'false');
        } else {
            wrapper.style.maxHeight = answer.scrollHeight + 'px';
            wrapper.classList.add('open');
            if (icon) {
                icon.classList.remove('bi-chevron-down');
                icon.classList.add('bi-chevron-up');
            }
            if (toggleBtn) toggleBtn.classList.add('open');
            if (questionBtn) questionBtn.setAttribute('aria-expanded', 'true');
        }
    }
});



/*  ========================================
  راهنمای کلی 

  templates/listings/listing_detail.html
  templates/listings/listing_list.html
   ========================================  */

document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.guide-question').forEach(function (row) {
        row.addEventListener('click', function () {
            const guideId = this.dataset.guideId;
            toggleGuide(guideId);
        });
    });

    function toggleGuide(guideId) {
        const wrapper = document.getElementById('guide-answer-wrapper-' + guideId);
        const answer = document.getElementById('guide-answer-' + guideId);
        const parentRow = document.querySelector(`.guide-question[data-guide-id="${guideId}"]`);
        const icon = parentRow.querySelector('.guide-icon');
        const toggleBtn = parentRow.querySelector('.guide-toggle-btn');
        const questionBtn = parentRow.querySelector('.guide-question-div');

        const isOpen = wrapper.classList.contains('open');

        if (isOpen) {
            wrapper.style.maxHeight = '0';
            wrapper.classList.remove('open');
            if (icon) {
                icon.classList.remove('bi-chevron-up');
                icon.classList.add('bi-chevron-down');
            }
            if (toggleBtn) toggleBtn.classList.remove('open');
            if (questionBtn) questionBtn.setAttribute('aria-expanded', 'false');
        } else {
            wrapper.style.maxHeight = answer.scrollHeight + 'px';
            wrapper.classList.add('open');
            if (icon) {
                icon.classList.remove('bi-chevron-down');
                icon.classList.add('bi-chevron-up');
            }
            if (toggleBtn) toggleBtn.classList.add('open');
            if (questionBtn) questionBtn.setAttribute('aria-expanded', 'true');
        }
    }
});




/*  ========================================
  تابع باز و بسته کردن بات تنظیمات برای انواع صفحات 

   templates/listings/listing_detail.html
   ========================================  */

function toggleHeight(cardId, closeHeight) {
    const aboutplatformCard = document.getElementById(`box-text-${cardId}`);
    const moreBtn = document.getElementById(`more-height-btn-${cardId}`);
    const myTextElement = document.getElementById(`text-more-card-${cardId}`);
    const BootStrap = document.getElementById(`bootstrap-${cardId}`);

    const isExpanded = aboutplatformCard.classList.toggle('expanded');
    moreBtn.classList.toggle('open');

    if (isExpanded) {
        // به جای 1000px، ارتفاع واقعی محتوا را محاسبه و اعمال می‌کنیم
        aboutplatformCard.style.maxHeight = aboutplatformCard.scrollHeight + 'px';

        if (myTextElement) myTextElement.innerText = '';
        if (BootStrap) BootStrap.style.display = 'none';
    } else {
        // ابتدا ارتفاع فعلی را ست می‌کنیم تا مرورگر بداند از چه عددی باید انیمیشن را شروع کند
        aboutplatformCard.style.maxHeight = aboutplatformCard.scrollHeight + 'px';

        // یک ترفند برای اعمال تغییر بلافاصله (Reflow)
        void aboutplatformCard.offsetHeight;

        // سپس ارتفاع را به مقدار بسته شدن تغییر می‌دهیم
        aboutplatformCard.style.maxHeight = closeHeight + 'px';

        if (myTextElement) myTextElement.innerText = '';
        if (BootStrap) BootStrap.style.display = 'none';
    }
}


// بررسی ارتفاع هنگام لود شدن صفحه
document.addEventListener("DOMContentLoaded", function () {
    checkContentHeight('1', 0, '1000px', 'open');
    checkContentHeight('2', 0, '1000px', 'closed');
    checkContentHeight('3', 0, '1000px', 'open');
    checkContentHeight('4', 0, '1000px', 'open');
    checkContentHeight('5', 0, '1000px', 'open');
    checkContentHeight('6', 0, '1000px', 'open');
    checkContentHeight('7', 0, '1000px', 'open');
    checkContentHeight('8', 0, '1000px', 'open');
    checkContentHeight('9', 0, '1000px', 'open');
    checkContentHeight('10', 0, '1000px', 'open');

});

function checkContentHeight(cardId, closeHeightNumber, openHeight, defaultState = 'closed') {
    const aboutplatformCard = document.getElementById(`box-text-${cardId}`);
    const moreBtn = document.getElementById(`more-height-btn-${cardId}`);
    const myTextElement = document.getElementById(`text-more-card-${cardId}`);
    const BootStrap = document.getElementById(`bootstrap-${cardId}`);

    // پیدا کردن هدر به صورت داینامیک برای حذف قابلیت کلیک
    const cardContainer = aboutplatformCard.closest('.aboutplatform-card');
    const headerElement = cardContainer ? cardContainer.querySelector('.aboutplatform-card-h3') : null;

    if (aboutplatformCard) {
        // بررسی اینکه آیا ارتفاع واقعی متن از ارتفاع مجاز حالت بسته کمتر یا مساوی است؟
        if (aboutplatformCard.scrollHeight <= closeHeightNumber) {
            // مخفی کردن دکمه ها و هاله رنگی
            if (myTextElement) myTextElement.style.display = 'none';
            if (BootStrap) BootStrap.style.display = 'none';
            if (moreBtn) moreBtn.style.display = 'none';

            // حذف قابلیت کلیک برای جلوگیری از باز و بسته شدن
            if (headerElement) {
                headerElement.onclick = null;
                headerElement.style.cursor = 'unset';
            }
            if (myTextElement) myTextElement.onclick = null;

            // برداشتن محدودیت ارتفاع
            aboutplatformCard.style.maxHeight = 'none';
        } else {
            // تنظیم وضعیت پیش‌فرض برای زمانی که متن طولانی است
            if (defaultState === 'open') {
                aboutplatformCard.classList.add('expanded');
                if (moreBtn) moreBtn.classList.add('open');

                // استفاده از ارتفاع واقعی به جای openHeight ثابت
                aboutplatformCard.style.maxHeight = aboutplatformCard.scrollHeight + 'px';

                if (myTextElement) myTextElement.innerText = '';
                if (BootStrap) BootStrap.style.display = 'none';
            } else {
                aboutplatformCard.style.maxHeight = closeHeightNumber + 'px';
            }
        }
    }
}



/* نمایش فقط ۴ تا از لینک در نوار دوم  */
/*     document.addEventListener('DOMContentLoaded', function () {
        const links = document.querySelectorAll('.scroll-link-navbar .text-link-scroll');
        const maxVisible = 4;

        links.forEach((link, index) => {
            if (index >= maxVisible) {
                link.style.display = 'none';
            }
        });
    }); */


/* دو ردیفه شدن text-link-scroll در نوار دوم */
function balanceNavbarLinks() {
    const navbar = document.querySelector('.scroll-link-navbar');
    if (!navbar) return; // جلوگیری از خطا در صورت پیدا نشدن عنصر

    const links = navbar.querySelectorAll('.text-link-scroll');
    const count = links.length;
    if (count === 0) return;

    const gap = 20; // gap بین لینک‌ها
    const maxSingleRowWidth = 800; // کمترین عرضی که بعدش دو ردیف می‌شه

    // عرض کل همه لینک‌ها
    let totalWidth = 0;
    for (let i = 0; i < count; i++) {
        totalWidth += links[i].offsetWidth;
    }
    totalWidth += gap * (count - 1);

    if (totalWidth <= maxSingleRowWidth) {
        // یک ردیف — max-width رو برمی‌داریم
        navbar.style.maxWidth = '100%'; // یا ''
        navbar.style.flexWrap = 'nowrap';
    } else {
        // دو ردیف 
        navbar.style.flexWrap = 'wrap';

        const half = Math.ceil(count / 2);
        let firstHalfWidth = 0;
        let secondHalfWidth = 0;

        // محاسبه عرض نیمه اول و دوم به صورت جداگانه
        for (let i = 0; i < count; i++) {
            if (i < half) {
                firstHalfWidth += links[i].offsetWidth;
            } else {
                secondHalfWidth += links[i].offsetWidth;
            }
        }

        // اضافه کردن گپ‌ها به هر ردیف
        firstHalfWidth += gap * (half - 1);
        const secondHalfCount = count - half;
        if (secondHalfCount > 0) {
            secondHalfWidth += gap * (secondHalfCount - 1);
        }

        // max-width برابر با بزرگترین ردیف + 2 پیکسل حاشیه اطمینان
        const maxRowWidth = Math.max(firstHalfWidth, secondHalfWidth) + 2;

        navbar.style.maxWidth = maxRowWidth + 'px';
    }
}

balanceNavbarLinks();













/*  ========================================
  فیلتر ها 

  templates/listings/listing_list.html
   ========================================  */

/*  اعمال فیلتر به صورت انی روی لیست اگهی ها */
document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("filterForm");
    let debounceTimer;

    form.querySelectorAll("input, select").forEach(function (el) {
        const eventType = (el.type === "checkbox" || el.tagName === "SELECT") ? "change" :
            "input";

        el.addEventListener(eventType, function () {
            if (el.type === "number" || el.type === "range") {
                clearTimeout(debounceTimer);
                debounceTimer = setTimeout(() => form.submit(), 2000);
            } else {
                form.submit();
            }
        });
    });
});





/*  نمایش رنج فیلتر ها */
document.querySelectorAll('.range-slider').forEach(slider => {
    const minInput = slider.querySelector('.range-min');
    const maxInput = slider.querySelector('.range-max');
    const fill = slider.querySelector('.range-fill');
    const minLabel = slider.querySelector('.range-val-min');
    const maxLabel = slider.querySelector('.range-val-max');
    const min = +slider.dataset.min;
    const max = +slider.dataset.max;

    function fmt(val) {
        return +val === max ? '∞' : Number(val).toLocaleString('en-us');
    }

    function update() {
        let lo = Math.min(+minInput.value, +maxInput.value);
        let hi = Math.max(+minInput.value, +maxInput.value);
        
        const pLo = (lo - min) / (max - min) * 100;
        const pHi = (hi - min) / (max - min) * 100;
        
        fill.style.right = pLo + '%'; 
        fill.style.left = 'auto'; 
        fill.style.width = (pHi - pLo) + '%';
        
        minLabel.textContent = fmt(lo);
        maxLabel.textContent = fmt(hi);
    }

    // جلوگیری از عبور حداقل از حداکثر
    minInput.addEventListener('input', (e) => {
        if (parseInt(minInput.value) >= parseInt(maxInput.value)) {
            minInput.value = maxInput.value;
        }
        update();
    });

    // جلوگیری از عبور حداکثر از حداقل
    maxInput.addEventListener('input', (e) => {
        if (parseInt(maxInput.value) <= parseInt(minInput.value)) {
            maxInput.value = minInput.value;
        }
        update();
    });

    update();
});





/*  ========================================
    گزینه اشتراک گزاری

   templates/listings/listing_list.html
   templates/listings/listing_detail.html
   ========================================  */

document.addEventListener("DOMContentLoaded", function() {
    const shareButtons = document.querySelectorAll('.share-listing-btn');

    shareButtons.forEach(button => {
        button.addEventListener('click', async function(e) {
            e.preventDefault(); // جلوگیری از رفتار پیش‌فرض
            
            const title = this.getAttribute('data-title');
            const url = this.getAttribute('data-url');

            // بررسی پشتیبانی مرورگر از قابلیت اشتراک‌گذاری (معمولا در موبایل)
            if (navigator.share) {
                try {
                    await navigator.share({
                        title: title,
                        text: 'این آگهی را بررسی کنید: ' + title,
                        url: url
                    });
                } catch (error) {
                    console.log('اشتراک‌گذاری لغو شد یا خطایی رخ داد', error);
                }
            } else {
                // در صورت عدم پشتیبانی مرورگر (مثل دسکتاپ)، لینک کپی شود
                navigator.clipboard.writeText(url).then(() => {
                    alert('لینک آگهی در حافظه کپی شد.');
                }).catch(err => {
                    console.error('خطا در کپی کردن لینک: ', err);
                });
            }
        });
    });
});




























/*  ========================================
    تنظیمات مربوط به نمایش نمودار ها 

    templates/listings/listing_detail.html
   ========================================  */

document.addEventListener('DOMContentLoaded', () => {
    const el = document.getElementById('chart-data');
    if (!el) return;

    const incomeRaw = el.dataset.income;
    const viewsRaw  = el.dataset.views;

    // ── تبدیل میلادی به شمسی ──────────────────────────────────
    function toJalali(year, month, day) {
        // الگوریتم تبدیل میلادی به جلالی
        const jy = year - 1600;
        const jm = month - 1;
        const jd = day - 1;

        let jDayNo = 365 * jy + Math.floor((jy + 3) / 4) - Math.floor((jy + 99) / 100) + Math.floor((jy + 399) / 400);
        for (let i = 0; i < jm; ++i)
            jDayNo += [31,28,31,30,31,30,31,31,30,31,30,31][i];
        if (jm > 1 && ((jy % 4 === 0 && jy % 100 !== 0) || jy % 400 === 0))
            ++jDayNo;
        jDayNo += jd;

        let jdi = jDayNo - 79;
        const jNp = Math.floor(jdi / 12053);
        jdi %= 12053;
        let jYear = 979 + 33 * jNp + 4 * Math.floor(jdi / 1461);
        jdi %= 1461;
        if (jdi >= 366) {
            jYear += Math.floor((jdi - 1) / 365);
            jdi = (jdi - 1) % 365;
        }
        let jMonth, jDay;
        const months = [31,31,31,31,31,31,30,30,30,30,30,29];
        for (let i = 0; i < 11; ++i) {
            if (jdi < months[i]) { jMonth = i + 1; jDay = jdi + 1; break; }
            jdi -= months[i];
        }
        if (jMonth === undefined) { jMonth = 12; jDay = jdi + 1; }
        return { year: jYear, month: jMonth, day: jDay };
    }

    // تبدیل رشته تاریخ (YYYY-MM-DD یا هر فرمت قابل parse) به شمسی
    function convertLabelToJalali(label) {
        // اگر label یک تاریخ میلادی باشه (مثلاً 2025-01-15 یا Jan 15)
        const isoMatch = label.match(/^(\d{4})-(\d{2})-(\d{2})$/);
        if (isoMatch) {
            const j = toJalali(+isoMatch[1], +isoMatch[2], +isoMatch[3]);
            return `${j.year}/${String(j.month).padStart(2,'0')}/${String(j.day).padStart(2,'0')}`;
        }
        // اگر فرمت دیگه‌ای بود، سعی می‌کنیم parse کنیم
        const d = new Date(label);
        if (!isNaN(d.getTime())) {
            const j = toJalali(d.getFullYear(), d.getMonth() + 1, d.getDate());
            return `${j.year}/${String(j.month).padStart(2,'0')}/${String(j.day).padStart(2,'0')}`;
        }
        // اگر قابل تبدیل نبود، همون label رو برمی‌گردونیم
        return label;
    }

    function convertLabels(labels) {
        return labels.map(convertLabelToJalali);
    }

    // ── فرمت‌کننده‌ها (اعداد انگلیسی) ────────────────────────
    function fmt(n) {
        if (n >= 1_000_000) return (n / 1_000_000).toFixed(1).replace(/\.0$/, '') + 'M';
        if (n >= 1_000)     return (n / 1_000).toFixed(1).replace(/\.0$/, '') + 'K';
        return Number(n).toLocaleString('en-US');
    }

    function fmtFull(n) {
        return Number(n).toLocaleString('en-US');
    }

    function avg(arr) {
        if (!arr.length) return 0;
        return arr.reduce((a, b) => a + b, 0) / arr.length;
    }

    // ── گرادیان ────────────────────────────────────────────────
    function makeGradient(ctx, area, c1, c2) {
        const gradient = ctx.createLinearGradient(0, area.top, 0, area.bottom);
        gradient.addColorStop(0, c1);
        gradient.addColorStop(1, c2);
        return gradient;
    }

    // ── پلاگین پس‌زمینه روشن ───────────────────────────────────
    const lightBgPlugin = {
        id: 'lightBg',
        beforeDraw(chart) {
            const { ctx, width, height } = chart;
            ctx.save();
            ctx.fillStyle = '#ffffff';
            ctx.fillRect(0, 0, width, height);
            ctx.restore();
        }
    };

    // ── پلاگین crosshair ────────────────────────────────────────
    const crosshairPlugin = {
        id: 'crosshair',
        afterDraw(chart) {
            if (!chart.tooltip?._active?.length) return;
            const { ctx, chartArea } = chart;
            const x = chart.tooltip._active[0].element.x;
            ctx.save();
            ctx.beginPath();
            ctx.moveTo(x, chartArea.top);
            ctx.lineTo(x, chartArea.bottom);
            ctx.lineWidth = 1;
            ctx.strokeStyle = 'rgba(0,0,0,0.12)';
            ctx.setLineDash([4, 4]);
            ctx.stroke();
            ctx.restore();
        }
    };

    // ── تنظیمات نمودار ──────────────────────────────────────────
    function buildOptions(unit, color) {
        return {
            responsive: true,
            maintainAspectRatio: false,
            interaction: { mode: 'index', intersect: false },
            plugins: {
                legend: { display: false },
                tooltip: {
                    rtl: true,
                    backgroundColor: 'rgba(255,255,255,0.97)',
                    titleColor: '#94a3b8',
                    bodyColor: '#1e293b',
                    borderColor: 'rgba(0,0,0,0.1)',
                    borderWidth: 1,
                    padding: { top: 8, bottom: 8, left: 12, right: 12 },
                    cornerRadius: 8,
                    displayColors: false,
                    titleFont: { family: 'Vazir, IRANSans, sans-serif', size: 11 },
                    bodyFont: { family: 'Vazir, IRANSans, sans-serif', size: 13, weight: 'bold' },
                    callbacks: {
                        title: items => items[0].label,
                        label: item => '  ' + fmtFull(item.raw) + ' ' + unit,
                    }
                }
            },
            scales: {
                x: {
                    grid: { display: false },
                    border: { display: false },
                    ticks: {
                        color: '#94a3b8',
                        font: { family: 'Vazir, IRANSans, sans-serif', size: 10 },
                        maxRotation: 40,
                        maxTicksLimit: 8,
                    }
                },
                y: {
                    position: 'left',
                    grid: { color: 'rgba(0,0,0,0.06)', drawBorder: false },
                    border: { display: false, dash: [4, 4] },
                    ticks: {
                        color: '#94a3b8',
                        font: { family: 'Vazir, IRANSans, sans-serif', size: 10 },
                        callback: v => fmt(v),
                        maxTicksLimit: 5,
                    },
                    beginAtZero: true,
                }
            },
            animation: {
                duration: 900,
                easing: 'easeInOutCubic',
            },
            elements: {
                line: { tension: 0.45 },
                point: {
                    radius: 3,
                    hoverRadius: 6,
                    hoverBorderWidth: 2,
                }
            }
        };
    }

    // ── ساخت نمودار ─────────────────────────────────────────────
    function buildChart(canvasId, data, color, gradientTop, gradientBot, unit, badgeId) {
        const canvas = document.getElementById(canvasId);
        if (!canvas) return;

        // تبدیل labels به شمسی
        const jalaliLabels = convertLabels(data.labels);

        let cachedGradient = null;
        let cachedArea     = null;

        new Chart(canvas, {
            type: 'line',
            plugins: [lightBgPlugin, crosshairPlugin],
            data: {
                labels: jalaliLabels,
                datasets: [{
                    data: data.data,
                    borderColor: color,
                    borderWidth: 2.5,
                    pointBackgroundColor: '#ffffff',
                    pointBorderColor: color,
                    pointBorderWidth: 2,
                    fill: true,
                    backgroundColor(context) {
                        const { ctx, chartArea } = context.chart;
                        if (!chartArea) return 'transparent';
                        const a = chartArea;
                        if (
                            !cachedGradient ||
                            cachedArea?.top    !== a.top    ||
                            cachedArea?.bottom !== a.bottom
                        ) {
                            cachedGradient = makeGradient(ctx, a, gradientTop, gradientBot);
                            cachedArea = { top: a.top, bottom: a.bottom };
                        }
                        return cachedGradient;
                    }
                }]
            },
            options: buildOptions(unit, color),
        });

        // به‌روزرسانی badge میانگین
        const badge = document.getElementById(badgeId);
        if (badge) {
            const mean = avg(data.data);
            badge.textContent = 'میانگین: ' + fmtFull(Math.round(mean)) + ' ' + unit;
        }
    }

    // ── بارگذاری داده‌های درآمد ─────────────────────────────────
    if (incomeRaw && incomeRaw !== 'None' && incomeRaw.trim() !== '') {
        try {
            const incomeData = JSON.parse(incomeRaw);
            if (incomeData?.labels?.length) {
                document.getElementById('income-chart-container').style.display = '';
                buildChart(
                    'incomeChart',
                    incomeData,
                    '#10b981',
                    'rgba(16,185,129,0.25)',
                    'rgba(16,185,129,0.02)',
                    'تومان',
                    'income-stat-badge'
                );
            }
        } catch (e) {
            console.error('income chart error:', e);
        }
    }

    // ── بارگذاری داده‌های بازدید ────────────────────────────────
    if (viewsRaw && viewsRaw !== 'None' && viewsRaw.trim() !== '') {
        try {
            const viewsData = JSON.parse(viewsRaw);
            if (viewsData?.labels?.length) {
                document.getElementById('views-chart-container').style.display = '';
                buildChart(
                    'viewsChart',
                    viewsData,
                    '#3b82f6',
                    'rgba(59,130,246,0.25)',
                    'rgba(59,130,246,0.02)',
                    'بازدید',
                    'views-stat-badge'
                );
            }
        } catch (e) {
            console.error('views chart error:', e);
        }
    }
});


/*  ========================================
   تنظیمات ظاهری مودار ها 
   ========================================  */

document.addEventListener('DOMContentLoaded', function () {
    const el = document.getElementById('chart-data');
    if (!el) return;

    const incomeRaw = el.getAttribute('data-income');
    const viewsRaw  = el.getAttribute('data-views');

    // فرمت عدد فارسی با واحد اختصاری
    function fmt(n) {
        n = Number(n);
        if (n >= 1_000_000) return (n / 1_000_000).toFixed(1) + 'M';
        if (n >= 1_000)     return (n / 1_000).toFixed(0) + 'K';
        return n.toLocaleString('fa-IR');
    }

    function fmtFull(n) {
        return Number(n).toLocaleString('fa-IR');
    }

    // محاسبه میانگین برای badge
    function avg(arr) {
        return arr.reduce((a, b) => a + b, 0) / arr.length;
    }

    // gradient
    function makeGradient(ctx, area, c1, c2) {
        const g = ctx.createLinearGradient(0, area.top, 0, area.bottom);
        g.addColorStop(0, c1);
        g.addColorStop(1, c2);
        return g;
    }

    // پلاگین پس‌زمینه تاریک canvas
    const darkBgPlugin = {
        id: 'darkBg',
        beforeDraw(chart) {
            const { ctx, width, height } = chart;
            ctx.save();
            ctx.fillStyle = '#1e293b';
            ctx.fillRect(0, 0, width, height);
            ctx.restore();
        }
    };

    // پلاگین خط عمودی hover
    const crosshairPlugin = {
        id: 'crosshair',
        afterDraw(chart) {
            if (!chart.tooltip._active || !chart.tooltip._active.length) return;
            const ctx = chart.ctx;
            const x = chart.tooltip._active[0].element.x;
            const top = chart.chartArea.top;
            const bottom = chart.chartArea.bottom;
            ctx.save();
            ctx.beginPath();
            ctx.moveTo(x, top);
            ctx.lineTo(x, bottom);
            ctx.lineWidth = 1.5;
            ctx.strokeStyle = 'rgba(255,255,255,0.15)';
            ctx.setLineDash([5, 4]);
            ctx.stroke();
            ctx.restore();
        }
    };

    function buildOptions(unit, color) {
        return {
            responsive: true,
            maintainAspectRatio: false,
            interaction: { mode: 'index', intersect: false },
            plugins: {
                legend: { display: false },
                tooltip: {
                    rtl: true,
                    backgroundColor: 'rgba(2, 8, 23, 0.95)',
                    titleColor: '#64748b',
                    bodyColor: '#f1f5f9',
                    borderColor: 'rgba(255,255,255,0.1)',
                    borderWidth: 1,
                    padding: { top: 10, bottom: 10, left: 14, right: 14 },
                    cornerRadius: 10,
                    displayColors: false,
                    titleFont: { family: 'Vazir, IRANSans, sans-serif', size: 11 },
                    bodyFont: { family: 'Vazir, IRANSans, sans-serif', size: 13, weight: 'bold' },
                    callbacks: {
                        title: items => items[0].label,
                        label: item => '  ' + fmtFull(item.raw) + ' ' + unit,
                    }
                },},
            scales: {
                x: {
                    grid: { display: false },
                    border: { display: false },
                    ticks: {
                        color: '#475569',
                        font: { family: 'Vazir, IRANSans, sans-serif', size: 10 },
                        maxRotation: 40,
                        maxTicksLimit: 8,
                    }
                },
                y: {
                    position: 'left',
                    grid: { color: 'rgba(255,255,255,0.05)', drawBorder: false },
                    border: { display: false, dash: [4, 4] },
                    ticks: {
                        color: '#475569',
                        font: { family: 'Vazir, IRANSans, sans-serif', size: 10 },
                        callback: v => fmt(v),
                        maxTicksLimit: 5,
                    },
                    beginAtZero: true,
                }
            },
            animation: { duration: 900, easing: 'easeInOutCubic' },
            elements: {
                line: { tension: 0.45, borderCapStyle: 'round' },
                point: {
                    radius: 3,
                    hoverRadius: 7,
                    hoverBorderWidth: 2.5,
                    hoverBackgroundColor: color,
                    hoverBorderColor: '#fff',
                }
            }
        };
    }

    function buildChart(canvasId, data, color, gradientTop, gradientBot, unit, badgeId, badgeUnit) {
        const canvas = document.getElementById(canvasId);
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        let grad = null;

        const chart = new Chart(ctx, {
            type: 'line',
            plugins: [darkBgPlugin, crosshairPlugin],
            data: {
                labels: data.labels,
                datasets: [{
                    data: data.data,
                    borderColor: color,
                    borderWidth: 2.5,
                    pointBackgroundColor: '#1e293b',
                    pointBorderColor: color,
                    pointBorderWidth: 2,
                    fill: true,
                    backgroundColor: function(context) {
                        const chart = context.chart;
                        const { ctx: c, chartArea } = chart;
                        if (!chartArea) return gradientTop;
                        if (!grad) grad = makeGradient(c, chartArea, gradientTop, gradientBot);
                        return grad;
                    },
                }]
            },
            options: buildOptions(unit, color),
        });

        // badge میانگین
        const avgVal = avg(data.data);
        const badge = document.getElementById(badgeId);
        if (badge) badge.textContent = 'میانگین: ' + fmtFull(Math.round(avgVal)) + ' ' + badgeUnit;

        return chart;
    }

    // درآمد
    if (incomeRaw && incomeRaw !== 'None' && incomeRaw !== '') {
        try {
            const d = JSON.parse(incomeRaw);
            if (d?.labels?.length) {
                document.getElementById('income-chart-container').style.display = 'block';
                buildChart(
                    'incomeChart', d,
                    '#10b981',
                    'rgba(16,185,129,0.4)',
                    'rgba(16,185,129,0.01)',
                    'تومان', 'income-stat-badge', 'تومان'
                );
            }
        } catch(e) { console.error(e); }
    }

    // بازدید
    if (viewsRaw && viewsRaw !== 'None' && viewsRaw !== '') {
        try {
            const d = JSON.parse(viewsRaw);
            if (d?.labels?.length) {
                document.getElementById('views-chart-container').style.display = 'block';
                buildChart(
                    'viewsChart', d,
                    '#3b82f6',
                    'rgba(59,130,246,0.4)',
                    'rgba(59,130,246,0.01)',
                    'بازدید', 'views-stat-badge', 'بازدید'
                );
            }
        } catch(e) { console.error(e); }
    }
});
