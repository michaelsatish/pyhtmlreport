def render_pie_chart(passed_tests, failed_tests, warning_tests):
    return """
            let ctx = document.getElementById("myPieChart");
            let myPieChart = new Chart(ctx, {
                type: 'pie',
                data: {
                    labels: ["Pass", "Fail", "Warning"],
                    datasets: [{
                        data: [%(passed)s, %(failed)s, %(warning)s],
                        backgroundColor: [
                            "#5cb85c",
                            "#d9534f",
                            "#f0ad4e"
                        ],
                        hoverBackgroundColor: [
                            "#5cb85c",
                            "#d9534f",
                            "#f0ad4e"
                        ],
                    }]
                },
            });
            """ % {'passed': passed_tests, 'failed': failed_tests, 'warning': warning_tests}

def render_overall_status_table(total_tests, passed_tests, failed_tests, warning_tests):
    return f"""
            <tr>
                <td>{total_tests}</td>
                <td>{passed_tests}</td>
                <td>{failed_tests}</td>
                <td>{warning_tests}</td>
            </tr>
            """
