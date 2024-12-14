const { Application, Assets, Sprite } = PIXI;

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

(async () =>
{
    // Create a new application
    const app = new Application();

    // Initialize the application
    await app.init({ background: '#fff', width: 128*4, height: 128*4 });

    // Append the application canvas to the document body
    document.body.appendChild(app.canvas);

    // Load the player texture
    const texture = await Assets.load('shield.png');
    const background = await Assets.load('dodgebackground.png');
    const box = await Assets.load('hitbox.png');

    // Create a player Sprite
    const player = new Sprite(box);
    const shield = new Sprite(texture);
    const bg = new Sprite(background);

    const wasd = [keyboard("w"), keyboard("a"), keyboard("s"), keyboard("d")];

    // Center the sprite's anchor point
    bg.anchor.set(0.5);
    player.anchor.set(0.5);
    shield.anchor.set(0.5)

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

    // Listen for animate update
    app.ticker.add((time) =>
    {
        // Just for fun, let's rotate mr rabbit a little.
        // * Delta is 1 if running at 100% performance *
        // * Creates frame-independent transformation *
        player.x += time.deltaTime * 3.0 * (wasd[3].isDown - wasd[1].isDown);
        player.y += time.deltaTime * 3.0 * (wasd[2].isDown - wasd[0].isDown);
        player.x = anchor(player.x, player.width / 2, app.screen.width - player.width / 2);
        player.y = anchor(player.y, player.height / 2, app.screen.height - player.height / 2);
    });
})();
