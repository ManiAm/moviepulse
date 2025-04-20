
document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".movie-card").forEach(card => {
        const id = card.dataset.id;
        const type = card.dataset.type;

        fetch(`/api/v1/${type}/${id}`)
            .then(res => res.json())
            .then(data => {
                const img = document.createElement("img");
                img.src = `https://image.tmdb.org/t/p/w500${data.poster_path}`;
                img.alt = data.title || data.name;
                card.prepend(img);

                const titleElem = card.querySelector(".media-title");
                if (titleElem) {
                    titleElem.textContent = data.title || data.name;
                }
            });

        const heart = card.querySelector(".favorite-heart");
        if (heart) {
            heart.addEventListener("click", (event) => {
                event.preventDefault();
                event.stopPropagation();

                const tmdb_id = card.dataset.id;
                const media_type = card.dataset.type;

                fetch("/api/v1/favorites", {
                    method: "DELETE",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ tmdb_id, media_type })
                }).then(res => res.json())
                  .then(data => {
                      if (data.success) {
                          // Remove the whole card + anchor from DOM
                          const wrapper = card.closest("a");
                          if (wrapper) {
                              wrapper.remove();
                          } else {
                              card.remove();
                          }
                      } else {
                          console.error("Failed to remove favorite:", data.message);
                      }
                  });
            });
        }
    });
});
