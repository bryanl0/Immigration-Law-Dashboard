import {
    Streamlit,
    StreamlitComponentBase,
    withStreamlitConnection
} from "streamlit-component-lib"
import * as React from "react"
import Button from "@mui/material/Button"
import styled from '@emotion/styled'


interface State {
    numClicks: number
}

class CustomMetric extends StreamlitComponentBase<State> {

    public state = {numClicks : 0}

    public render = (): React.ReactNode => {
        const StyledButton = styled(Button)({
            margin: "0px 0px 10px 0px",
        });
        return (
            <span>
                <StyledButton variant="contained"
                onClick={this.onClicked}>Hello World</StyledButton>
            </span>
        );
    }

    private onClicked = (): void => {
        this.setState(
            prevState => ({numClicks: prevState.numClicks + 1}),
            () => Streamlit.setComponentValue(this.state.numClicks)
        )
    }
}

export default withStreamlitConnection(CustomMetric)