class Table:
    def __init__(
        self, headers: list[str], records: list[dict[str, str]], unit: str
    ) -> None:
        self.headers = headers
        self.records = records
        self.unit = unit

    def create_headers(self) -> str:
        return (
            "<tr>"
            + '<th scope="col"></th>'
            + "".join([f'<th scope="col">{header}</th>' for header in self.headers])
            + "</tr>"
        )

    def create_records(self) -> list[str]:
        return [
            "".join([f"<td>{value}{self.unit}</td>" for value in record])
            for record in self.records
        ]

    def wrap_records_with_headers(self, records: list[str]) -> str:
        rows_html = ""
        for index, row in enumerate(records):
            rows_html += "<tr>"
            rows_html += f'<th scope="row">{index}</th>'
            rows_html += row
            rows_html += "</tr>"
        return rows_html

    def calculate_averages(self) -> list[float]:
        sums = [0.0 for _ in self.headers]
        for record in self.records:
            for i, value in enumerate(record):
                sums[i] += float(value)
        return [round(sum / len(self.records), 2) for sum in sums]

    def create_footer(self, averages: list[float]) -> str:
        return (
            "<tr>"
            + '<th scope="row">Avg</th>'
            + "".join([f"<td>{average}{self.unit}</td>" for average in averages])
            + "</tr>"
        )

    def render(self) -> str:
        headers_html = self.create_headers()
        records_html = self.create_records()
        rows_html = self.wrap_records_with_headers(records_html)
        averages = self.calculate_averages()
        footer_html = self.create_footer(averages)
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
