window.observerFlag = false;
let observedElement = document.querySelector(".jquery_server_clock");
let currentTime = observedElement.textContent.trim();
console.log("Setting up observer for: ", observedElement);

function convertTo24HourFormat(timeString) {
  let [_, hours, minutes, seconds, meridian] = timeString.match(
    /(\d+):(\d+):(\d+) (AM|PM)/
  );
  if (meridian === "PM" && hours !== "12") hours = Number(hours) + 12;
  if (meridian === "AM" && hours === "12") hours = "00";
  return Number(
    `${String(hours).padStart(2, "0")}${String(minutes).padStart(
      2,
      "0"
    )}${String(seconds).padStart(2, "0")}`
  );
}

function isTimePastOrEqual(currentTimeString, serverTimeString) {
  let current = convertTo24HourFormat(currentTimeString);
  let server = convertTo24HourFormat(serverTimeString);
  console.log(current, server);
  return current >= server;
}

let observer = new MutationObserver((mutations) => {
  let currentTime = observedElement.textContent.trim();
  if (isTimePastOrEqual(currentTime, "##SERVER_TIME##")) {
    window.observerFlag = true;
    window.currentTime = currentTime;
    observer.disconnect();
  }
});

if (isTimePastOrEqual(currentTime, "##SERVER_TIME##")) {
  window.observerFlag = true;
  window.currentTime = currentTime;
} else {
  observer.observe(observedElement, {
    childList: true,
  });
}
