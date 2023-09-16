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
import { DrawerProps } from "@suid/material/Drawer";
import { toggleDrawerHOC, DrawerHOCstate, DrawerHOC } from "~/shared/components/Drawer";

export const toggleDrawerHelp = (e) => toggleDrawerHOC("help", !DrawerHOCstate["help"], DrawerHOCstate)(e);

export default function HelperDrawer(props:DrawerProps) {

  const anchorPos = 'bottom'


  const list = () => (
    <Box
      sx={{ width: "auto" }}
      role="presentation"
      onClick={toggleDrawerHelp}
      onKeyDown={toggleDrawerHelp}
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
      drawer="help"
      anchor={anchorPos}
      open={DrawerHOCstate["options"]}
      sx={{ zIndex: 9999 }}
      onClose={toggleDrawerHelp}
    >
      {list()}
    </DrawerHOC>
  );
}