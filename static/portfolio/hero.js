(() => {
    const scene = document.querySelector('#web-build');
    if (!scene) return;
    const replay = document.querySelector('#web-build-replay');
    const motion = window.matchMedia('(prefers-reduced-motion: reduce)');
    let arrangeTimer;
    let finishTimer;
    let observer;
    let frame;

    function finish() {
        clearTimeout(arrangeTimer);
        clearTimeout(finishTimer);
        cancelAnimationFrame(frame);
        scene.classList.remove('is-scattered', 'is-animating');
        replay.disabled = false;
        replay.hidden = motion.matches;
    }

    function play() {
        if (motion.matches) return finish();
        clearTimeout(arrangeTimer);
        clearTimeout(finishTimer);
        scene.classList.remove('is-animating');
        scene.classList.add('is-scattered');
        replay.disabled = true;
        replay.hidden = false;
        // Two frames preserve the starting composition when replaying.
        frame = requestAnimationFrame(() => {
            frame = requestAnimationFrame(() => {
                scene.classList.add('is-animating');
                arrangeTimer = setTimeout(() => {
                    scene.classList.remove('is-scattered');
                    finishTimer = setTimeout(finish, 2600);
                }, 1600);
            });
        });
    }

    replay.addEventListener('click', play);
    motion.addEventListener('change', () => {
        if (motion.matches) {
            if (observer) observer.disconnect();
            finish();
        } else {
            replay.hidden = false;
        }
    });
    if (motion.matches) return finish();
    if ('IntersectionObserver' in window) {
        observer = new IntersectionObserver(entries => {
            if (!entries.some(entry => entry.isIntersecting)) return;
            observer.disconnect();
            play();
        }, { threshold: .35 });
        observer.observe(scene);
    } else {
        play();
    }
})();
