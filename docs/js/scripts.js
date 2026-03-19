window.addEventListener('load', function() {

    // --- Navigation: Hamburger + Mobile Dropdowns ---
    var menuToggle = document.querySelector('.menu-toggle');
    var navMenu = document.querySelector('nav');

    if (menuToggle && navMenu) {

        menuToggle.addEventListener('click', function(e) {
            e.stopPropagation();
            navMenu.classList.toggle('active');
            menuToggle.setAttribute('aria-expanded', navMenu.classList.contains('active'));
        });

        navMenu.addEventListener('click', function(e) {
            if (e.target === navMenu) {
                navMenu.classList.remove('active');
                menuToggle.setAttribute('aria-expanded', 'false');
                navMenu.querySelectorAll('.dropdown').forEach(function(d) {
                    d.classList.remove('open');
                });
            }
        });

        navMenu.querySelectorAll('a:not(.dropdown > a)').forEach(function(link) {
            link.addEventListener('click', function() {
                navMenu.classList.remove('active');
                menuToggle.setAttribute('aria-expanded', 'false');
                navMenu.querySelectorAll('.dropdown').forEach(function(d) {
                    d.classList.remove('open');
                });
            });
        });

        navMenu.querySelectorAll('.dropdown > a').forEach(function(link) {
            link.addEventListener('click', function(e) {
                if (window.innerWidth <= 768) {
                    e.preventDefault();
                    e.stopPropagation();
                    var parentLi = this.parentElement;
                    var wasOpen = parentLi.classList.contains('open');
                    navMenu.querySelectorAll('.dropdown').forEach(function(d) {
                        d.classList.remove('open');
                    });
                    if (!wasOpen) {
                        parentLi.classList.add('open');
                    }
                }
            });
        });
    }

    // --- End Navigation ---
});


// --- Shared initialisation on DOM ready ---
document.addEventListener('DOMContentLoaded', function() {

    // Load shared footer on all pages
    var placeholder = document.getElementById('footer-placeholder');
    if (placeholder) {
        fetch('_footer.html')
            .then(function(response) {
                if (!response.ok) throw new Error('Footer load failed');
                return response.text();
            })
            .then(function(data) {
                placeholder.innerHTML = data;
            })
            .catch(function(error) {
                console.error('Error loading footer:', error);
            });
    }

    // Volunteer roles — only runs if elements exist on the page
    var rolesContent = document.getElementById('roles-content');
    if (rolesContent) {
        fetch('roles.json')
            .then(function(response) {
                if (!response.ok) throw new Error('Could not load roles.json');
                return response.json();
            })
            .then(function(roles) {
                generateRoleContent(roles);
                attachRoleClickListener();
            })
            .catch(function(error) {
                console.error('Error loading roles:', error);
                rolesContent.innerHTML = '<p style="padding: 20px; color: red; font-weight: bold;">Error: Failed to load opportunities. Please check the roles.json file.</p>';
            });
    }

});


// --- Volunteer role functions ---
function attachRoleClickListener() {
    const rolesNav = document.getElementById('roles-nav');
    if (rolesNav) {
        rolesNav.addEventListener('click', (event) => {
            const clickedButton = event.target.closest('.tab-button');
            if (clickedButton) {
                const roleId = clickedButton.getAttribute('data-role-id');
                showRoleDetails(roleId, clickedButton);
            }
        });
    }
}

function showRoleDetails(roleId, clickedButtonElement) {
    document.querySelectorAll('.role-advert').forEach(advert => advert.classList.add('hidden'));
    document.querySelectorAll('.tab-button').forEach(button => button.classList.remove('active'));

    const selectedAdvert = document.getElementById(roleId);
    if (selectedAdvert) selectedAdvert.classList.remove('hidden');
    if (clickedButtonElement) clickedButtonElement.classList.add('active');
}

function generateRoleContent(roles) {
    const rolesNav = document.getElementById('roles-nav');
    const rolesContent = document.getElementById('roles-content');

    if (!rolesNav || !rolesContent) return;

    rolesContent.innerHTML = '';

    roles.forEach((role, index) => {
        const isActive = index === 0;
        const buttonClass = isActive ? 'tab-button active' : 'tab-button';

        rolesNav.insertAdjacentHTML('beforeend', `
            <button class="${buttonClass}" data-role-id="${role.id}">
                <strong>${role.title}</strong>
                <p>${role.subtitle}</p>
            </button>
        `);

        const advertClass = isActive ? 'role-advert active' : 'role-advert hidden';
        const mailtoLink = `mailto:hello@tennisnerds.org?subject=${role.linkSubject}`;
        const detailsList = role.details.map(detail => `<li>${detail}</li>`).join('');

        rolesContent.insertAdjacentHTML('beforeend', `
            <article id="${role.id}" class="${advertClass}">
                <h2>${role.heading}</h2>
                <p>${role.description}</p>
                <ul>${detailsList}</ul>
                <a href="${mailtoLink}" class="cta-button ${role.buttonClass}">${role.linkText}</a>
            </article>
        `);
    });

    if (roles.length > 0) {
        const firstButton = document.querySelector(`.tab-button[data-role-id="${roles[0].id}"]`);
        showRoleDetails(roles[0].id, firstButton);
    }
}


fetch('_footer.html')
    .then(function(response) {
        if (!response.ok) throw new Error('Footer load failed');
        return response.text();
    })
    .then(function(data) {
        console.log('Footer length:', data.length);
        console.log('Footer content:', data);
        var placeholder = document.getElementById('footer-placeholder');
        if (placeholder) {
            placeholder.innerHTML = data;
        }
    })
    .catch(function(error) {
        console.error('Error loading footer:', error);
    });