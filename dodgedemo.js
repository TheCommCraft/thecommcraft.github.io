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

(async () =>
{
    // Create a new application
    const app = new Application();

    // Initialize the application
    await app.init({ background: '#1099bb', resizeTo: window });

    // Append the application canvas to the document body
    document.body.appendChild(app.canvas);

    // Load the bunny texture
    const texture = await Assets.load('https://pixijs.com/assets/bunny.png');

    // Create a bunny Sprite
    const bunny = new Sprite(texture);

    const wasd = [keyboard("w"), keyboard("a"), keyboard("s"), keyboard("d")];

    // Center the sprite's anchor point
    bunny.anchor.set(0.5);

    // Move the sprite to the center of the screen
    bunny.x = app.screen.width / 2;
    bunny.y = app.screen.height / 2;

    app.stage.addChild(bunny);

    // Listen for animate update
    app.ticker.add((time) =>
    {
        // Just for fun, let's rotate mr rabbit a little.
        // * Delta is 1 if running at 100% performance *
        // * Creates frame-independent transformation *
        bunny.position.x += time.deltaTime * 3.0 * (wasd[3].isDown - wasd[1].isDown);
        bunny.position.y += time.deltaTime * 3.0 * (wasd[2].isDown - wasd[0].isDown);
    });
})();
