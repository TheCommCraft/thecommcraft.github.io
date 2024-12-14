const { Application, Assets, Sprite, Point } = PIXI;

function keyboard(value) {
  const key = {};
  key.value = value;
  key.isDown = false;
  key.isUp = true;
  key.press = undefined;
  key.release = undefined;
  //The `downHandler`
  key.downHandler = (event) => {
    if (event.key === key.value) {
      if (key.isUp && key.press) {
        key.press();
      }
      key.isDown = true;
      key.isUp = false;
      event.preventDefault();
    }
  };

  //The `upHandler`
  key.upHandler = (event) => {
    if (event.key === key.value) {
      if (key.isDown && key.release) {
        key.release();
      }
      key.isDown = false;
      key.isUp = true;
      event.preventDefault();
    }
  };

  //Attach event listeners
  const downListener = key.downHandler.bind(key);
  const upListener = key.upHandler.bind(key);
  
  window.addEventListener("keydown", downListener, false);
  window.addEventListener("keyup", upListener, false);
  
  // Detach event listeners
  key.unsubscribe = () => {
    window.removeEventListener("keydown", downListener);
    window.removeEventListener("keyup", upListener);
  };
  
  return key;
}

function anchor(x, a, b) {
  return Math.max(Math.min(x, b), a);
}

function makeCross(pos) {
  const crossSprite = new Sprite(crossAsset);
  app.stage.addChild(crossSprite)
  crossSprite.position = pos;
  crossSprite.countdown = 60;
  crossSprite.anchor.set(0.5);
  return crossSprite;
}

(async () =>
{
    // Create a new application
    window.app = new Application();

    // Initialize the application
    await app.init({ background: '#fff', width: 128*4, height: 128*4 });

    // Append the application canvas to the document body
    document.getElementById("demo").appendChild(app.canvas);

    // Load the player texture
    const texture = await Assets.load('shield.png');
    const background = await Assets.load('dodgebackground.png');
    const box = await Assets.load('hitbox.png');
    window.crossAsset = await Assets.load('cross.png');

    // Create a player Sprite
    const player = new Sprite(box);
    const shield = new Sprite(texture);
    const bg = new Sprite(background);

    const wasd = [keyboard("w"), keyboard("a"), keyboard("s"), keyboard("d")];


    // Center the sprite's anchor point
    bg.anchor.set(0.5);
    player.anchor.set(0.5);
    shield.anchor.set(0.5);

    // Move the sprite to the center of the screen
    player.x = app.screen.width / 2;
    player.y = app.screen.height / 2;
    bg.x = app.screen.width / 2;
    bg.y = app.screen.height / 2;
    shield.x = app.screen.width / 2;
    shield.y = app.screen.height / 2;

    app.stage.addChild(bg);
    app.stage.addChild(player);
    app.stage.addChild(shield);

    let countdown = 30.0;
    window.crosses = [];

    let mousePos = new Point(app.screen.width / 2, app.screen.width / 2);
    app.stage.eventMode = 'static';
    app.stage.hitArea = app.screen;
    app.stage.on("mousemove", (event) => {mousePos = event.global;})

    // Listen for animate update
    app.ticker.add((time) =>
    {
        // Just for fun, let's rotate mr rabbit a little.
        // * Delta is 1 if running at 100% performance *
        // * Creates frame-independent transformation *
        countdown -= time.deltaTime;
        if (countdown <= 0) {
          countdown = Math.random() * 30;
          crosses.push(makeCross(new Point(crossAsset.width / 2 + Math.random() * (app.screen.width - crossAsset.width), crossAsset.height / 2 + Math.random() * (app.screen.height - crossAsset.height))));
        }
        player.x += time.deltaTime * 4.0 * (wasd[3].isDown - wasd[1].isDown);
        player.y += time.deltaTime * 4.0 * (wasd[2].isDown - wasd[0].isDown);
        player.x = anchor(player.x, player.width / 2 + 12, app.screen.width - player.width / 2 - 12);
        player.y = anchor(player.y, player.height / 2 + 12, app.screen.height - player.height / 2 - 12);
        shield.position = mousePos;
        shield.x = anchor(shield.x, player.x - player.width / 2 + shield.width / 2 + 4, player.x + player.width / 2 - shield.width / 2 - 4);
        shield.y = anchor(shield.y, player.y - player.width / 2 + shield.height / 2 + 4, player.y + player.height / 2 - shield.height / 2 - 4);
        for (const cross of crosses.values()) {
          if (cross.countdown > 30) {
            cross.visible = !((cross.countdown / 5) % 2);
          }
          else if (cross.countdown > 15) {
            cross.visible = !((cross.countdown / 3) % 2);
          }
          else if (cross.countdown > 5) {
            cross.visible = !((cross.countdown / 2) % 2);
          }
          else if (cross.countdown >= 0) {
            cross.visible = !(cross.countdown % 2);
          }
          else {
            app.stage.removeChild(cross);
            crosses.splice(crosses.indexOf(cross), 1)
          }
        }
    });
})();
