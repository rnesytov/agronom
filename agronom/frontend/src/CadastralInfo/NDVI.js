import React from "react";
import axios from "axios";
import * as moment from "moment";
import { List, ListItem, ListItemText } from "@material-ui/core";

class NDVI extends React.Component {
  state = {
    ndvi: []
  };

  componentDidMount() {
    axios
      .get("/api/v0_1/ndvi/", { params: { field_id: this.props.field.id } })
      .then(res => {
        this.setState({ ndvi: res.data });
      });
  }

  handleClick = () => {
    console.log("IT'S A CLICK!!!");
  };

  render() {
    if (this.state.ndvi.length > 0) {
      return (
        <List>
          {this.state.ndvi.map((n, i) => (
            <ListItem key={i} button>
              <ListItemText
                primary={moment(n.date, "YYYY-MM-DD").format("MMMM Do YYYY")}
                secondary={`Среднее значение: ${n.mean}`}
                onClick={() => {
                  this.props.showNDVI(n);
                }}
              />
            </ListItem>
          ))}
        </List>
      );
    } else {
      return <span>NDVI не заргужен</span>;
    }
  }
}

export default NDVI;
