window.observerFlag = false;
let observedElement = document.querySelector(".jquery_server_clock");
console.log("Setting up observer for: ", observedElement);

function convertTo24HourFormat(timeString) {
  console.log("timeString:", timeString); // Debugging line to check the actual content of timeString.
  let match = timeString.match(/(\d+):(\d+):(\d+) (AM|PM)/);
  if (match !== null) {
    let [_, hours, minutes, seconds, meridian] = match;
    // Continue with the rest of your logic.
  } else {
    console.error("Invalid time format:", timeString);
  }

  let [_, hours, minutes, seconds, meridian] = timeString.match(
    /(\d+):(\d+):(\d+) (AM|PM)/
  );
  if (meridian === "PM" && hours !== "12") hours = Number(hours) + 12;
  if (meridian === "AM" && hours === "12") hours = "00";
  return `${hours}:${minutes}:${seconds}`;
}

function isTimePastOrEqual(currentTimeString, serverTimeString) {
  let current = convertTo24HourFormat(currentTimeString);
  let server = convertTo24HourFormat(serverTimeString);
  return current >= server;
}

let observer = new MutationObserver((mutations) => {
  let currentTime = observedElement.textContent.trim();
  console.log("Watching the clock. Current time is " + currentTime);
  if (isTimePastOrEqual(currentTime, "##SERVER_TIME##")) {
    window.observerFlag = true;
    window.currentTime = currentTime;
    observer.disconnect();
  }
});

let currentTime = observedElement.textContent.trim();
if (isTimePastOrEqual(currentTime, "##SERVER_TIME##")) {
  window.observerFlag = true;
  window.currentTime = currentTime;
} else {
  observer.observe(observedElement, {
    childList: true,
  });
}
