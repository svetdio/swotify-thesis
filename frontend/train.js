$(function () {
    $('#sa_train').unbind('click').on('click', function () {
        let url = $('#csv_url').val();

        let isTrain = confirm("Are you sure you want to train this data?")
        if (isTrain) {
            $('#train-form').busyLoad("show", {
                spinner: "accordion"
            });
            train(url);
        }
    })

    const train = function (url) {
        const evtSource = new EventSource(`http://localhost:8000/train?csv_url=${encodeURIComponent(url)}`);
        const eventList = document.querySelector("ul");

        const newElement = document.createElement("li");
        newElement.innerHTML = `<p class="has-text-link">Initializing training process.. this might take a while...</p>`;
        eventList.appendChild(newElement);

        evtSource.addEventListener('mlstep', function (event) {
            steps = JSON.parse(event.data);
            const newElement = document.createElement("li");
            newElement.innerHTML = `${steps.message}`;
            eventList.appendChild(newElement);
        });

        evtSource.addEventListener('mlerror', function (event) {
            steps = JSON.parse(event.data);
            const newElement = document.createElement("li");
            newElement.innerHTML = `<p class="has-text-danger">${steps.message}</p>`;
            eventList.appendChild(newElement);
            evtSource.close()
            $('#train-form').busyLoad("hide");
        });


        evtSource.addEventListener('mlfinish', function (event) {
            steps = JSON.parse(event.data);
            const newElement = document.createElement("li");
            newElement.innerHTML = `<p class="has-text-success">${steps.message}</p>`;
            eventList.appendChild(newElement);
            evtSource.close();
            $('#train-form').busyLoad("hide");
        });

        evtSource.onerror = (error) => {
            console.error('EventSource failed', error)

            const newElement = document.createElement("li");
            newElement.innerHTML = `<p class="has-text-danger">Something wrong happened during the training. Model training will be aborted.</p>`;
            eventList.appendChild(newElement);

            evtSource.close()
            $('#train-form').busyLoad("hide");
        }
    }
});