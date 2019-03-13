import React from "react";
import { Typography } from "@material-ui/core"

export default function ({ loadingState }) {
  let color, text;

  switch (loadingState) {
    case 0:
      color = "primary";
      text = "Ожидание загрузки инфрмацаии из реестра";
      break;
    case 1:
      color = "default";
      text = "Информация из реестра загружена";
      break;
    case 2:
      color = "error";
      text = "Не удалось загрузить информацию из реестра";
      break;
    default:
      color = "error";
      text = "Ошибка";
      break;
  }

  return (
    <Typography
      component="p"
      color={color}
    >
      {text}
    </Typography>
  );
}
