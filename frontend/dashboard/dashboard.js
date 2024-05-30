$(function () {
    // Chart.register(ChartDataLabels)

    $("#csg-officers").autocomplete({
        source: function (request, response) {
            $.ajax({
                url: "http://localhost:8000/get_officers_names",
                data: {
                    keyword: request.term
                },
                success: function (data) {
                    response(data.officers);
                }
            });
        },
    });


    $('#sa_evaluate').unbind('click').on("click", function () {
        let evaluatee = $('#csg-officers').val();
        if (evaluatee == "") {
            alert('Please put name of evaluatee')
        } else {
            fetch('http://localhost:8000/get_sentiment_values/' + evaluatee)
                .then(response => response.json())
                .then(data => {
                    $.each($('p.main_score'), function (i, d) {
                        $(d).html(data[$(d).attr('id')]);
                    })

                    sentimentDistribution(data.positive_sentiment, data.neutral_sentiment, data.negative_statement);
                    return fetch('http://localhost:8000/get_performance_rating/' + evaluatee)
                })
                .then(response => response.json())
                .then(data => {
                    performanceRatings(data)
                });
        }

    })

    const getMax = function (object) {
        return Object.keys(object)
            .filter(x => {
                return object[x] == Math.max.apply(null,
                    Object.values(object));
            })
    }

    const getMin = function (object) {
        return Object.keys(object)
            .filter(x => {
                return object[x] == Math.min.apply(null,
                    Object.values(object));
            })
    }

    const sentimentDistribution = function (positive, neutral, negative) {
        let chartStatus = Chart.getChart("sentiment_distribution");
        if (chartStatus != undefined) {
            chartStatus.destroy();
        }

        return new Chart(
            document.getElementById('sentiment_distribution'),
            {
                type: 'pie',
                data: {
                    labels: ['Negative', 'Neutral', 'Positive'],
                    datasets: [{
                        data: [negative, neutral, positive],
                        backgroundColor: [
                            'hsl(348, 100%, 61%)',
                            'hsl(204, 86%, 53%)',
                            'hsl(141, 71%, 48%)',
                        ],
                        hoverOffset: 4
                    }]
                },
                plugins: [ChartDataLabels],
                options: {
                    responsive: true,
                    // aspectRatio: 1,
                    plugins: {
                        datalabels: {
                            formatter: (value, ctx) => {
                                const val = (typeof value == 'undefined' || value == 0) ? 0 : value;
                                const datapoints = ctx.chart.data.datasets[0].data
                                const total = datapoints.reduce((total, datapoint) => total + (typeof datapoint == 'undefined' ? 0 : datapoint), 0)
                                const percentage = val / total * 100
                                return (percentage == 0) ? '' : percentage.toFixed(2) + "%";
                            },
                            color: 'black',
                        }
                    }
                }
            });
    }

    const performanceRatings = function (data) {
        let chartStatus = Chart.getChart("performance_ratings");
        if (chartStatus != undefined) {
            chartStatus.destroy();
        }

        const labels = [
            'Responsibility',
            'Team Communication',
            'Task Delegation',
            'Calmness',
            'Adaptability',
            'Attitude',
            'Internal Collaboration',
            'External Response',
            'Time Management',
            'External Collaboration',
            'Flexibility',
            'Accountability'
        ]

        const perf_ratings = [
            data.responsibility_rating,
            data.team_communication_rating,
            data.task_delegation_rating,
            data.calmness_rating,
            data.adaptability_rating,
            data.attitude_rating,
            data.comm_collab_rating,
            data.external_resp_rating,
            data.time_management_rating,
            data.collab_rating,
            data.flexible_rating,
            data.accountability_rating,
        ]

        const colors = []
        const bestPerf = getMax(data);
        const worstPerf = getMin(data);

        for (const [rating, val] of Object.entries(data)) {
            if (bestPerf.includes(rating)) {
                colors.push('hsl(141, 71%, 48%)')
            } else if (worstPerf.includes(rating)) {
                colors.push('hsl(348, 100%, 61%)')
            } else {
                colors.push('hsl(204, 86%, 53%)')
            }
        }

        return new Chart(
            document.getElementById('performance_ratings'),
            {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [{
                        data: perf_ratings,
                        backgroundColor: colors,
                        hoverOffset: 4
                    }]
                },
                options: {
                    indexAxis: 'y',
                    responsive: true,
                    aspectRatio: 3,
                    plugins: {
                        legend: {
                            display: false
                        },
                    }
                }
            });
    }
});