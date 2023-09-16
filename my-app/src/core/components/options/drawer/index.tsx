import MailIcon from "@suid/icons-material/Mail";
import InboxIcon from "@suid/icons-material/MoveToInbox";
import {
  Box,
  Divider,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
} from "@suid/material";
import { DrawerProps } from "@suid/material/Drawer/DrawerProps";
import { toggleDrawerHOC, DrawerHOCstate, DrawerHOC } from "~/shared/components/Drawer";

export const toggleDrawerOptions = () => toggleDrawerHOC("options", DrawerHOCstate["options"], DrawerHOCstate);

export default function OptionsDrawer(props:DrawerProps) {

  const anchorPos = 'left'


  const list = () => (
    <Box
      sx={{ width: "auto" }}
      role="presentation"
      onClick={toggleDrawerOptions}
      onKeyDown={toggleDrawerOptions}
    >
      <List>
        {["Inbox", "Starred", "Send email", "Drafts"].map((text, index) => (
          <ListItem disablePadding>
            <ListItemButton>
              <ListItemIcon>
                {index % 2 === 0 ? <InboxIcon /> : <MailIcon />}
              </ListItemIcon>
              <ListItemText primary={text} />
            </ListItemButton>
          </ListItem>
        ))}
      </List>
      <Divider />
      <List>
        {["All mail", "Trash", "Spam"].map((text, index) => (
          <ListItem disablePadding>
            <ListItemButton>
              <ListItemIcon>
                {index % 2 === 0 ? <InboxIcon /> : <MailIcon />}
              </ListItemIcon>
              <ListItemText primary={text} />
            </ListItemButton>
          </ListItem>
        ))}
      </List>
    </Box>
  );

  return (
    <DrawerHOC
      drawer="options"
      anchor={anchorPos}
      open={DrawerHOCstate[anchorPos]}
      sx={{ zIndex: 9999 }}
      onClose={toggleDrawerOptions}
    >
      {list()}
    </DrawerHOC>
  );
}