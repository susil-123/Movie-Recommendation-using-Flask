document.addEventListener('keydown', (event) => {
    if (event.key === ' ') {
        console.log('Space is pressed');
        const spotlight = document.querySelector('.spotlight');
        const main = document.querySelector('.main')
        const inputField = document.querySelector('.inp--spotlight')
        spotlight.classList.remove('hidden');
        main.classList.add('spotlight-div')
        inputField.focus();
        document.addEventListener('keydown',e=>{
            if(e.key === 'Enter'){
                let movieName = inputField.value.trim(); // Trim to remove leading/trailing whitespace
                movieName = encodeURIComponent(movieName); // Encode the parameter
                const currentUrl = window.location.href;
                const newUrl = new URL(currentUrl);
                newUrl.pathname = 'recommend_page/'; // Ensure the path is correct
                newUrl.searchParams.set('movie_name', movieName); // Set the query parameter
            
                window.location.replace(newUrl.toString());
            }
        })
    }
    else if (event.key === 'Escape') {
        console.log('Space is pressed');
        const spotlight = document.querySelector('.spotlight');
        const main = document.querySelector('.main')
        spotlight.classList.add('hidden');
        main.classList.remove('spotlight-div')
    }
});

document.addEventListener('DOMContentLoaded', () => {
    const posters = document.querySelectorAll('.poster-small');
    posters.forEach(poster => {
        poster.addEventListener('click', () => {
            const movieName = poster.id; // Get the ID of the clicked poster element
            if (movieName) {
                const encodedMovieName = encodeURIComponent(movieName); // Ensure proper encoding
                const currentUrl = window.location.href;
                const newUrl = new URL(currentUrl);
                newUrl.pathname = 'recommend_page/'; // Adjust the path to match your Flask route
                newUrl.searchParams.set('movie_name', encodedMovieName); // Set the query parameter

                // Redirect to the new URL
                window.location.href = newUrl.toString();
            }
        });
    });
});


