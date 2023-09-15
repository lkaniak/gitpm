import MailIcon from "@suid/icons-material/Mail";
import InboxIcon from "@suid/icons-material/MoveToInbox";
import {
  Box,
  Button,
  Divider,
  Drawer,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
} from "@suid/material";

import { createMutable } from "solid-js/store";
import { FlowComponent, FlowProps } from "solid-js";
import { DrawerProps } from "@suid/material/Drawer";

export type DrawerCompProps = DrawerProps & FlowProps;
export type DrawerAnchor = NonNullable<DrawerProps["anchor"]>;

export const toggleDrawerHOC =
  (anchor: DrawerAnchor, open: boolean, state: { [K in DrawerAnchor]: boolean; }) => (event: MouseEvent | KeyboardEvent) => {
    if (event.type === "keydown") {
      const keyboardEvent = event as KeyboardEvent;
      if (keyboardEvent.key === "Tab" || keyboardEvent.key === "Shift")
        return;
    }
    state[anchor] = open;
  };

export const DrawerHOCstate = createMutable<{
    [K in DrawerAnchor]: boolean;
  }>({
    top: false,
    left: false,
    bottom: false,
    right: false,
  });

export const DrawerHOC: FlowComponent<DrawerCompProps> = (props) => {

  return (
    <Drawer
      anchor="bottom"
      open={DrawerHOCstate[props.anchor]}
      sx={{ zIndex: 9999 }}
      onClose={toggleDrawerHOC(props.anchor, false, DrawerHOCstate)}
    >
      {props.children}
    </Drawer>
  );
}