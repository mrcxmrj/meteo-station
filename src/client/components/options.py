class Options:
    def __init__(self) -> None:
        pass

    def render(self):
        return """
            <form action="/set-options" method="post">
                <fieldset>
                    <label>
                        Refresh rate (ms)
                        <input type="number" id="refresh-rate" name="refresh-rate" placeholder="1000" aria-label="Number" />
                    </label>
                </fieldset>
                <input type="submit" value="Save" />
            </form>
        """
