// static/js/main.js

function debounce(fn, delay) {
    let timeout;
    return (...args) => {
        clearTimeout(timeout);
        timeout = setTimeout(() => fn(...args), delay);
    };
}

document.addEventListener("DOMContentLoaded", () => {

    // Restore scroll position and highlight clicked card
    const savedScroll = sessionStorage.getItem("scrollPosition");
    const restoreToTop = sessionStorage.getItem("restoreToTop");
    
    if (savedScroll !== null && restoreToTop === "false") {
        window.scrollTo(0, parseInt(savedScroll));
        sessionStorage.removeItem("scrollPosition");
        sessionStorage.removeItem("restoreToTop");
    }    

    const clickedCardId = sessionStorage.getItem("clickedCardId");

    if (clickedCardId) {
        const clickedCard = document.getElementById(clickedCardId);
        if (clickedCard) {
            clickedCard.classList.add("highlighted-card");
        }
        sessionStorage.removeItem("clickedCardId");
    }

    fetch("/api/v1/trending/movies")
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById("movies-container");

            data.forEach(movie => {
                const card = document.createElement("div");
                card.className = "movie-card";
                card.id = `movie-${movie.id}`;

                const poster = movie.poster_path 
                    ? `<img src="https://image.tmdb.org/t/p/w500${movie.poster_path}" alt="${movie.title}">`
                    : `<div>No Image</div>`;

                card.innerHTML = `
                <a href="/movie/${movie.id}" style="text-decoration: none; color: inherit;">
                    ${poster}
                    <h3>${movie.title}</h3>
                    <p>${movie.release_date}</p>
                    <p>⭐ ${Math.round(movie.vote_average * 10)}%</p>
                </a>
                `;

                // Save scroll position before navigating
                card.addEventListener("click", () => {
                    sessionStorage.setItem("scrollPosition", window.scrollY);
                    sessionStorage.setItem("clickedCardId", `movie-${movie.id}`);
                });

                container.appendChild(card);
            });
        })
        .catch(err => {
            console.error("Failed to fetch trending movies", err);
        });

    // Trending TV Shows
    fetch("/api/v1/trending/tv")
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById("tv-container");

            data.forEach(tv => {
                const card = document.createElement("div");
                card.className = "movie-card";
                card.id = `tv-${tv.id}`;

                const poster = tv.poster_path
                    ? `<img src="https://image.tmdb.org/t/p/w500${tv.poster_path}" alt="${tv.name}">`
                    : `<div>No Image</div>`;

                card.innerHTML = `
                    <a href="/tv/${tv.id}" style="text-decoration: none; color: inherit;">
                        ${poster}
                        <h3>${tv.name}</h3>
                        <p>${tv.first_air_date}</p>
                        <p>⭐ ${Math.round(tv.vote_average * 10)}%</p>
                    </a>
                `;                

                card.addEventListener("click", () => {
                    sessionStorage.setItem("scrollPosition", window.scrollY);
                    sessionStorage.setItem("clickedCardId", `tv-${tv.id}`);
                });

                container.appendChild(card);
            });
        });


    fetch("/api/v1/discover/popular")
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById("movies-popular");

            data.forEach(movie => {
                const card = document.createElement("div");
                card.className = "movie-card";
                card.id = `movie-popular-${movie.id}`;

                const poster = movie.poster_path 
                    ? `<img src="https://image.tmdb.org/t/p/w500${movie.poster_path}" alt="${movie.title}">`
                    : `<div>No Image</div>`;

                card.innerHTML = `
                <a href="/movie/${movie.id}" style="text-decoration: none; color: inherit;">
                    ${poster}
                    <h3>${movie.title}</h3>
                    <p>${movie.release_date}</p>
                    <p>⭐ ${Math.round(movie.vote_average * 10)}%</p>
                </a>
                `;

                // Save scroll position before navigating
                card.addEventListener("click", () => {
                    sessionStorage.setItem("scrollPosition", window.scrollY);
                    sessionStorage.setItem("clickedCardId", `movie-popular-${movie.id}`);
                });

                container.appendChild(card);
            });
        })
        .catch(err => {
            console.error("Failed to fetch trending movies", err);
        });

    fetch("/api/v1/discover/upcoming")
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById("movies-upcoming");

            data.forEach(movie => {
                const card = document.createElement("div");
                card.className = "movie-card";
                card.id = `movie-upcoming-${movie.id}`;

                const poster = movie.poster_path 
                    ? `<img src="https://image.tmdb.org/t/p/w500${movie.poster_path}" alt="${movie.title}">`
                    : `<div>No Image</div>`;

                card.innerHTML = `
                <a href="/movie/${movie.id}" style="text-decoration: none; color: inherit;">
                    ${poster}
                    <h3>${movie.title}</h3>
                    <p>${movie.release_date}</p>
                    <p>⭐ ${Math.round(movie.vote_average * 10)}%</p>
                </a>
                `;

                // Save scroll position before navigating
                card.addEventListener("click", () => {
                    sessionStorage.setItem("scrollPosition", window.scrollY);
                    sessionStorage.setItem("clickedCardId", `movie-upcoming-${movie.id}`);
                });

                container.appendChild(card);
            });
        })
        .catch(err => {
            console.error("Failed to fetch trending movies", err);
        });

    fetch("/api/v1/discover/top_rated")
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById("movies-top-rated");

            data.forEach(movie => {
                const card = document.createElement("div");
                card.className = "movie-card";
                card.id = `movie-top-rated-${movie.id}`;

                const poster = movie.poster_path 
                    ? `<img src="https://image.tmdb.org/t/p/w500${movie.poster_path}" alt="${movie.title}">`
                    : `<div>No Image</div>`;

                card.innerHTML = `
                <a href="/movie/${movie.id}" style="text-decoration: none; color: inherit;">
                    ${poster}
                    <h3>${movie.title}</h3>
                    <p>${movie.release_date}</p>
                    <p>⭐ ${Math.round(movie.vote_average * 10)}%</p>
                </a>
                `;

                // Save scroll position before navigating
                card.addEventListener("click", () => {
                    sessionStorage.setItem("scrollPosition", window.scrollY);
                    sessionStorage.setItem("clickedCardId", `movie-top-rated-${movie.id}`);
                });

                container.appendChild(card);
            });
        })
        .catch(err => {
            console.error("Failed to fetch trending movies", err);
        });

    fetch("/api/v1/discover/adults")
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById("movies-adults");

            data.forEach(movie => {
                const card = document.createElement("div");
                card.className = "movie-card";
                card.id = `movie-adults-${movie.id}`;

                const poster = movie.poster_path 
                    ? `<img src="https://image.tmdb.org/t/p/w500${movie.poster_path}" alt="${movie.title}">`
                    : `<div>No Image</div>`;

                card.innerHTML = `
                <a href="/movie/${movie.id}" style="text-decoration: none; color: inherit;">
                    ${poster}
                    <h3>${movie.title}</h3>
                    <p>${movie.release_date}</p>
                    <p>⭐ ${Math.round(movie.vote_average * 10)}%</p>
                </a>
                `;

                // Save scroll position before navigating
                card.addEventListener("click", () => {
                    sessionStorage.setItem("scrollPosition", window.scrollY);
                    sessionStorage.setItem("clickedCardId", `movie-adults-${movie.id}`);
                });

                container.appendChild(card);
            });
        })
        .catch(err => {
            console.error("Failed to fetch trending movies", err);
        });

});


document.getElementById("search-input").addEventListener("input", debounce(async (e) => {
    const query = e.target.value.trim();
    const resultsContainer = document.getElementById("search-results");
    resultsContainer.innerHTML = ""; // Clear previous

    if (query.length < 2) return;

    const response = await fetch(`/api/v1/search?query=${encodeURIComponent(query)}`);
    const data = await response.json();

    data
        .filter(item => item.media_type !== "person")
        .forEach(item => {
        if (!item.poster_path && !item.profile_path) return;

        const card = document.createElement("div");
        card.className = "movie-card";
        const image = item.poster_path || item.profile_path;
        const title = item.title || item.name;
        const type = item.media_type;

        const poster = `<img src="https://image.tmdb.org/t/p/w500${image}" alt="${title}">`;

        let href = "#";
        if (type === "movie") href = `/movie/${item.id}`;
        else if (type === "tv") href = `/tv/${item.id}`;

        card.innerHTML = `
            <a href="${href}" style="text-decoration: none; color: inherit;">
                ${poster}
                <h3>${title}</h3>
                <p>Type: ${type}</p>
            </a>
        `;

        // Scroll memory
        card.addEventListener("click", () => {
            sessionStorage.setItem("scrollPosition", window.scrollY);
            sessionStorage.setItem("clickedCardId", `search-${item.id}`);
        });

        card.id = `search-${item.id}`;
        resultsContainer.appendChild(card);
    });
}, 400)); // debounce to avoid API spamming
