import {
    Streamlit,
    StreamlitComponentBase,
    withStreamlitConnection
} from "streamlit-component-lib"
import React, {ReactNode} from "react"

interface State {
    numClicks: number
}

class CustomMetric extends StreamlitComponentBase<State> {

    public state = {numClicks : 0}

    public render = (): ReactNode => {
        return (
            <button 
            style={{marginLeft:20, marginTop:20, marginBottom:20}}
            onClick={this.onClicked}>
                Hello World
            </button>
        )
    }

    private onClicked = (): void => {
        this.setState(
            prevState => ({numClicks: prevState.numClicks + 1}),
            () => Streamlit.setComponentValue(this.state.numClicks)
        )
    }
}

export default withStreamlitConnection(CustomMetric)