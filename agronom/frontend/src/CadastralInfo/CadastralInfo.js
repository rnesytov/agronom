import {
  Paper,
  withStyles,
  Drawer,
  AppBar,
  Tabs,
  Tab
} from "@material-ui/core";
import axios from "axios";
import L from "leaflet";
import React from "react";
import { FeatureGroup, Map, Polygon, TileLayer, GeoJSON } from "react-leaflet";
import { EditControl } from "react-leaflet-draw";
import EditField from "./EditField";
import Weather from "./Weather"

const styles = {
  map: {
    height: "90vh"
  },
  drawer: {
    width: 480
  }
};

class CadastralInfo extends React.Component {
  state = {
    cadLoaded: false,
    cadastral: {},
    fieldsLoaded: false,
    fields: [],
    editDrawerOpen: false,
    currentField: {},
    tabValue: 0
  };

  componentDidMount() {
    this.loadCadastral();
    this.loadFields();
  }

  loadCadastral() {
    axios
      .get(`/api/v0_1/cadastral/${this.props.match.params.id}/`)
      .then(res => {
        const cadastral = res.data;
        this.setState({ cadastral, cadLoaded: true });
        document.title = `Участок ${cadastral.cadastral_number}`;
      });
  }

  loadFields() {
    axios
      .get(`/api/v0_1/cadastral/${this.props.match.params.id}/fields/`)
      .then(res => {
        const fields = res.data;
        this.setState({ fields, fieldsLoaded: true });
      });
  }

  addField(geoJSON) {
    axios
      .post(`/api/v0_1/cadastral/${this.props.match.params.id}/fields/`, {
        polygon: geoJSON.geometry
      })
      .then(res => {
        this.loadFields();
        this.showEditDrawer(res.data);
      });
  }

  deleteField = () => {
    axios
      .delete(`/api/v0_1/cadastral/${this.props.match.params.id}/fields/`, {
        data: { id: this.state.currentField.id }
      })
      .then(() => {
        this.hideEditDrawer();
        this.loadFields();
      });
  };

  updateField = field => {
    axios
      .put(`/api/v0_1/cadastral/${this.props.match.params.id}/fields/`, field)
      .then(() => {
        this.hideEditDrawer();
        this.loadFields();
      });
  };

  showEditDrawer = field => {
    this.setState({ editDrawerOpen: true, currentField: field });
  };

  hideEditDrawer = () => {
    this.setState({ editDrawerOpen: false, currentField: {} });
  };

  getBounds = () => {
    const poly = this.state.cadastral.polygon;

    return L.geoJSON(poly)
      .getBounds();
  };

  _onCreate = e => {
    const geoJSON = e.layer.toGeoJSON();

    this.addField(geoJSON);
  };

  handleTabChange = (event, tabValue) => {
    this.setState({ tabValue });
  };

  render() {
    const { classes } = this.props;

    if (this.state.cadLoaded && this.state.fieldsLoaded) {
      return (
        <Paper>
          <Map bounds={this.getBounds()}  className={classes.map}>
            <TileLayer url="http://mt0.google.com/vt/lyrs=s,h&x={x}&y={y}&z={z}" />
            {this.state.cadastral.polygon.coordinates}
            <GeoJSON
              data={this.state.cadastral.polygon}
              fill={false}
              color="#fff"
              weight={2}
            />
            <FeatureGroup>
              <EditControl
                position="topright"
                onEdited={this._onEdit}
                onCreated={this._onCreate}
                onDeleted={this._onDelete}
                edit={{ edit: false, remove: false }}
                draw={{
                  polyline: false,
                  rectangle: false,
                  circle: false,
                  marker: false,
                  circlemarker: false,
                  polygon: {
                    allowIntersection: false,
                    shapeOptions: { weight: 1 }
                  }
                }}
              />
              {this.state.fields.map(f => (
                <Polygon
                  key={f.id}
                  positions={L.GeoJSON.coordsToLatLngs(
                    f.polygon.coordinates,
                    1
                  )}
                  onclick={() => {
                    this.showEditDrawer(f);
                  }}
                  weight={1}
                  color={f.color}
                />
              ))}
            </FeatureGroup>
          </Map>
          <Drawer
            anchor="left"
            open={this.state.editDrawerOpen}
            onClose={this.hideEditDrawer}
          >
            <div className={classes.drawer}>
              <AppBar position="static">
                <Tabs
                  value={this.state.tabValue}
                  onChange={this.handleTabChange}
                >
                  <Tab label="Поле" />
                  <Tab label="Погода" />
                  <Tab label="NDVI" disabled />
                </Tabs>
              </AppBar>
              {this.state.tabValue === 0 && (
                <EditField
                  field={this.state.currentField}
                  handleDelete={this.deleteField}
                  handleSubmit={this.updateField}
                />
              )}
              {this.state.tabValue === 1 && (
                <Weather field={this.state.currentField} />
              )}
            </div>
          </Drawer>
        </Paper>
      );
    } else {
      return "Загрузка карты";
    }
  }
}

export default withStyles(styles)(CadastralInfo);
