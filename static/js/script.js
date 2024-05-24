function activateModal () { 
    document.addEventListener('DOMContentLoaded', () => {
    let graphInfoButton = document.getElementById("graph-info-btn");
    let graphInfoModal = document.querySelector(".graph-info-modal");
    let closeButton = document.querySelector(".close");
    
    graphInfoButton.addEventListener('click', () => {
        graphInfoModal.style.display = 'block';
    });
    
    closeButton.addEventListener('click', () => {
        graphInfoModal.style.display = 'none';
    });
   
    window.addEventListener('click', (event) => {
        if (event.target === graphInfoModal) {
            graphInfoModal.style.display = 'none';
        }
        });
    });
}

activateModal()
