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

  render() {
    if (this.state.ndvi.length > 0) {
      return (
        <List>
          {this.state.ndvi.map((n, i) => (
            <ListItem
              key={i}
              button
              onClick={() => {
                this.props.showNDVI(n);
              }}
            >
              <ListItemText
                primary={`Среднее значение: ${n.mean}`}
                secondary={moment(n.date, "YYYY-MM-DD").format(
                  "D.M.YYYY"
                )}
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
