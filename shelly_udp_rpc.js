let EVENT_NAME = "em_reading";
let EM_ID = 2; // matches shelly_em_key "em1:2" — the CT clamp feeding the ESP

function timerHandler(user_data) {
  let em = Shelly.getComponentStatus("em1", EM_ID);
  Shelly.emitEvent(EVENT_NAME, {
    act_power: em.act_power,
    current: em.current,
    voltage: em.voltage
  });
}

Timer.set(1000, true, timerHandler, null);
