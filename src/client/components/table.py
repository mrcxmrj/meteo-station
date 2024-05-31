class Table:
    def __init__(self, headers: list[str], records: list[list[str]], unit: str) -> None:
        self.headers = headers
        self.records = records
        self.unit = unit

    def render(self) -> str:
        headers_html: str = (
            "<tr>"
            + '<th scope="col"></th>'
            + "".join([f'<th scope="col">{header}</th>' for header in self.headers])
            + "</tr>"
        )
        records_html: list[str] = [
            "".join([f"<td>{value}{self.unit}</td>" for value in record])
            for record in self.records
        ]

        rows_html = ""
        for index, row in enumerate(records_html):
            rows_html += "<tr>"
            rows_html += f'<th scope="row">{index}</th>'
            rows_html += row
            rows_html += "</tr>"

        sums = [0.0 for _ in self.headers]
        for record in self.records:
            for i, value in enumerate(record):
                sums[i] += float(value)
        averages = [round(sum / len(self.records), 2) for sum in sums]
        footer_html: str = (
            "<tr>"
            + '<th scope="row">Average</th>'
            + "".join([f"<td>{average}{self.unit}</td>" for average in averages])
            + "</tr>"
        )

        return f"""
            <table class="striped">
                <thead>
                    {headers_html}
                </thead>
                <tbody>
                    {rows_html}
                </tbody>
                <tfoot>
                    {footer_html}
                </tfoot>
            </table>
        """
