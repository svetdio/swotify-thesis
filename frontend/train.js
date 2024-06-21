$(function () {
    $('#sa_train').unbind('click').on('click', function () {
        let url = $('#csv_url').val();

        let isTrain = confirm("Are you sure you want to train this data?")
        if (isTrain) {
            train(url);
        }
    })

    const train = function (url) {
        const evtSource = new EventSource(`http://localhost:8000/train?csv_url=${encodeURIComponent(url)}`);
        const eventList = document.querySelector("ul");

        evtSource.addEventListener('mlstep', function (event) {
            steps = JSON.parse(event.data);
            const newElement = document.createElement("li");
            newElement.innerHTML = `${steps.message}`;
            eventList.appendChild(newElement);
        });


        evtSource.addEventListener('mlfinish', function (event) {
            steps = JSON.parse(event.data);
            const newElement = document.createElement("li");
            newElement.innerHTML = `${steps.message}`;
            eventList.appendChild(newElement);
            evtSource.close();
        });

        evtSource.onerror = (error) => {
            console.error('EventSource failed', error)
            evtSource.close()
        }
    }
});