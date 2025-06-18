document.addEventListener('DOMContentLoaded', function() {
    // Обработка мобильного меню
    const filterSidebarOpen = document.querySelector('.header_filterSidebar_open');
    const filterSidebar = document.querySelector('.header_filterSidebar');
    
    if (filterSidebarOpen && filterSidebar) {
        filterSidebarOpen.addEventListener('click', function() {
            filterSidebar.style.display = filterSidebar.style.display === 'none' ? 'block' : 'none';
        });
    }

    // Обработка форм
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;

            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    isValid = false;
                    field.classList.add('error');
                } else {
                    field.classList.remove('error');
                }
            });

            if (!isValid) {
                e.preventDefault();
                alert('Пожалуйста, заполните все обязательные поля');
            }
        });
    });

    // Обработка загрузки изображений
    const imageInputs = document.querySelectorAll('input[type="file"]');
    imageInputs.forEach(input => {
        input.addEventListener('change', function(e) {
            const files = e.target.files;
            const preview = document.querySelector(`#${input.id}-preview`);
            
            if (preview && files.length > 0) {
                preview.innerHTML = '';
                Array.from(files).forEach(file => {
                    if (file.type.startsWith('image/')) {
                        const reader = new FileReader();
                        reader.onload = function(e) {
                            const img = document.createElement('img');
                            img.src = e.target.result;
                            img.style.maxWidth = '200px';
                            img.style.margin = '5px';
                            preview.appendChild(img);
                        };
                        reader.readAsDataURL(file);
                    }
                });
            }
        });
    });

    // Обработка фильтров
    const filterInputs = document.querySelectorAll('.filter-input');
    filterInputs.forEach(input => {
        input.addEventListener('change', function() {
            const form = input.closest('form');
            if (form) {
                form.submit();
            }
        });
    });

    // Обработка календаря бронирования
    const dateInputs = document.querySelectorAll('input[type="date"]');
    dateInputs.forEach(input => {
        input.addEventListener('change', function() {
            const startDate = document.querySelector('#start_date');
            const endDate = document.querySelector('#end_date');
            
            if (startDate && endDate) {
                if (new Date(endDate.value) < new Date(startDate.value)) {
                    endDate.value = startDate.value;
                }
            }
        });
    });

    // Обработка уведомлений
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            setTimeout(() => {
                alert.remove();
            }, 300);
        }, 5000);
    });

    const addListingBtn = document.querySelector('.main_list_addButton');
    
    if (addListingBtn) {
        console.log('Кнопка найдена');
        console.log('Информация о пользователе:', window.currentUser);
        
        addListingBtn.addEventListener('click', function() {
            console.log('Кнопка нажата');
            console.log('Текущий пользователь:', window.currentUser);
            
            if (window.currentUser && window.currentUser.is_authenticated) {
                console.log('Пользователь авторизован');
                console.log('Тип пользователя:', window.currentUser.user_type);
                
                if (window.currentUser.user_type === 'landlord') {
                    console.log('Перенаправление на создание объявления');
                    window.location.href = '/listings/create';
                } else {
                    console.log('Показ сообщения для арендатора');
                    alert('Для размещения объявлений необходимо зарегистрироваться как арендодатель. Пожалуйста, выйдите из системы и зарегистрируйтесь заново с типом пользователя "Арендодатель".');
                }
            } else {
                console.log('Пользователь не авторизован, перенаправление на регистрацию');
                window.location.href = '/register';
            }
        });
    } else {
        console.log('Кнопка не найдена');
    }
}); 