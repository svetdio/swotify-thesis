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
            $('#loading-screen').addClass('is-hidden');
            $('#results-pane').removeClass('is-hidden');


            fetch('http://localhost:8000/get_sentiment_values/' + evaluatee)
                .then(response => response.json())
                .then(data => {
                    $.each($('p.main_score'), function (i, d) {
                        $(d).html(data[$(d).attr('id')]);
                    })
                    sentimentDistribution(data.positive_sentiment, data.neutral_sentiment, data.negative_sentiment);

                    return fetch('http://localhost:8000/get_performance_rating/' + evaluatee)
                })
                .then(response => response.json())
                .then(data => {
                    performanceRatings(data)

                    return fetch('http://localhost:8000/get_comments/' + evaluatee)
                })
                .then(response => response.json())
                .then(data => {
                    renderComments(data)
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
                    plugins: {
                        datalabels: {
                            formatter: (value, ctx) => {
                                const val = (typeof value == 'undefined' || value == 0) ? 0 : value;
                                const datapoints = ctx.chart.data.datasets[0].data
                                const total = datapoints.reduce((total, datapoint) => total + (typeof datapoint == 'undefined' ? 0 : datapoint), 0)
                                const percentage = val / total * 100
                                // debugger;
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

        const user_perf_ratings = [
            data.self.responsibility_rating,
            data.self.team_communication_rating,
            data.self.task_delegation_rating,
            data.self.calmness_rating,
            data.self.adaptability_rating,
            data.self.attitude_rating,
            data.self.comm_collab_rating,
            data.self.external_resp_rating,
            data.self.time_management_rating,
            data.self.collab_rating,
            data.self.flexible_rating,
            data.self.accountability_rating,
        ]

        const global_perf_ratings = [
            data.global.responsibility_rating,
            data.global.team_communication_rating,
            data.global.task_delegation_rating,
            data.global.calmness_rating,
            data.global.adaptability_rating,
            data.global.attitude_rating,
            data.global.comm_collab_rating,
            data.global.external_resp_rating,
            data.global.time_management_rating,
            data.global.collab_rating,
            data.global.flexible_rating,
            data.global.accountability_rating,
        ]

        return new Chart(
            document.getElementById('performance_ratings'),
            {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Personal Performance',
                        data: user_perf_ratings,
                        backgroundColor: 'hsl(204, 86%, 53%)',
                        hoverOffset: 4
                    },
                    {
                        label: 'Overall Performance',
                        data: global_perf_ratings,
                        backgroundColor: 'hsl(0, 0%, 86%)',
                        hoverOffset: 4
                    }
                    ]
                },
                options: {
                    indexAxis: 'y',
                    responsive: true,
                    aspectRatio: 3,
                    plugins: {
                        legend: {
                            display: true,
                        }
                    },
                }
            });
    }

    const renderComments = function (data) {
        if ($.fn.DataTable.isDataTable('#sentiment_comments')) {
            $('#sentiment_comments').DataTable().destroy();
        }

        let tbl_content = "";

        for (const d of data) {
            tbl_content += "<tr>";
            tbl_content += "<td>" + d.evaluator + "</td>";
            tbl_content += "<td>" + d.event_contribution + "</td>";
            tbl_content += "<td>" + d.comment_feedback + "</td>";
            tbl_content += "</tr>";
        }
        $('#sentiment_comments tbody').html(tbl_content);

        $('#sentiment_comments').DataTable({
            responsive: true,
            lengthMenu: [
                [5, 10, -1],
                [5, 10, 'All']
            ]
        });
    }
});