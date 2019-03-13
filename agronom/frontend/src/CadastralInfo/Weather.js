import React from "react";
import axios from "axios";
import * as moment from "moment";
import { List, ListItem, ListItemText, Avatar } from "@material-ui/core";

class Weather extends React.Component {
  state = {
    weather: []
  };

  componentDidMount() {
    axios
      .get("/api/v0_1/weather/", { params: { field_id: this.props.field.id } })
      .then(res => {
        this.setState({ weather: res.data });
      });
  }

  render() {
    if (this.state.weather.length > 0) {
      return (
        <List>
          {this.state.weather.map(w => (
            <ListItem key={w.id}>
              <Avatar src={w.data.hourly[0].weatherIconUrl[0].value} />
              <ListItemText
                secondary={moment(w.date, "YYYY-MM-DD").format(
                  "MMMM Do YYYY"
                )}
                primary={w.data.maxtempC}
              />
            </ListItem>
          ))}
        </List>
      );
    } else {
      return <span>Погода еще не загружена</span>;
    }
  }
}

export default Weather;
