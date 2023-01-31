# Welcome to Chorumfur-Bot

## What Am I?
Chorumfur-Bot is a database-backed custom discord bot implemented in discord.py to facilitate the Discord sim-game **Chorumfurs**.

## Commands
### Game Commands
`.joinGame` - Adds you to the game's database and allows you to participate in the game.
`.me` - Displays details about your user account
`.help` - Displays a help message detailing the bot's capabilities.  Use `.help <command>` for more details about a particular command.

### Chorumfur Commands
`.myLair` - Displays a list of all of your chorumfurs.
`.getCreature <creature id>` - Displays detailed information about the chorumfur whose ID you specify.
`.giveCreature <creature ID> @user` - Gives a chorumfur with the ID you specify to the user you @mention.
`.renameCreature <creature ID> <new name>` - Updates a Chorumfur's name in the database.

### Breeding Commands
`.crystal` - Displays how many days until your breeding crystal is fully charged.  You need a fully charged crystal to breed chorumfurs.
`.breed <parent A> <parent B>` - Initiates a request for breeding for two chorumfurs.  If you don't own both of the creatures in question, it will submit a request to the owner of the other chorumfur.  **Your breeding crystal isn't consumed until the recipient of the request agrees to the pairing.**

Breed requests are sent to the artist for fulfillment (see **Ticket Commands** below)
`.acceptBreeding <Ticket ID>` - Accept a request for someone to breed their chorumfur with yours.  You'll be @ mentioned when a request for breeding is created.  If you wait more than 30 days to respond, the ticket is automatically cancelled.
`.declineBreeding <Ticket ID>` - The inverse of the above.  This command declines another user's request for breeding.  When you decline a breeding, the ticket is immediately cancelled and the user is notified of your decision.

### Ticket Commands
`.myTickets` - Displays a list of all of your breeding requests.
`.getTicket <Ticket ID>` - Displays more data about a given ticket.
`.cancelTicket <Ticket ID>` - Cancels an in-progress ticket.  **This cannot be reversed, be careful!**

### Inventory Commands
`.inventory` - Displays all of the items in your inventory
`.getItem <Item ID>` - Displays details about an item
`.shop` - **COMING SOON** Displays the shop interface so that you can buy items.
`.wallet` - **COMING SOON** Displays the amount of currency in your wallet.

### Admin Commands
*These commands will only work for users with the `Admin` role.*
`.addItemToInv <Item ID> <user_id> <quantity>` - Adds an item to a specified user in a specified quantity.  If no user ID is specified, adds the item to your inventory.  If no quantity is specified, adds one.
`.removeItemFromInv <Item ID> <user_id> <quantity>` - Removes an item from a specified user in a specified quantity.  If no user ID is specified, removes the item from your inventory.  If no quantity is specified, removes one.
`.makeCreature <name> <main horn> <cheek horn> <face horn> <tail> <tail tip> <fluff> <mutation> <owner>` - Adds a custom creature to the game.  The `owner` parameter is optional.  If not included, adds the chorumfur to your lair.
`.makeRandomCreature <name>` - Creates a fully randomized chorumfur and adds them to your lair.
`.adminBreed <creature a> <creature b>` - Adds a breeding request to the ticket queue without draining a user's breeding crystal.
`.updateImage <creature ID> <URL of image>` - Replaces an existing chorumfur image with a new one specified by the user.
`.advanceTicket <Ticket ID>` - Advances a ticket's status to the next type
`.showTickets <open|pending>` - Displays a summary view of all tickets in the queue.  Can show all **open** tickets or only ones **pending** artist work.
`.getDetailedTicket <Ticket ID>` - Displays a detailed view of a given ticket.  Includes all of the details of the chorumfur litter.
`.getAllItems` - Displays a list of all items currently implemented in the game.