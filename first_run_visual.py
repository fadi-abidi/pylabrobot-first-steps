import asyncio

from pylabrobot.liquid_handling import LiquidHandler
from pylabrobot.liquid_handling.backends import LiquidHandlerChatterboxBackend
from pylabrobot.visualizer import Visualizer
from pylabrobot.resources import (
  STARLetDeck,
  TIP_CAR_480_A00,
  PLT_CAR_L5AC_A00,
  hamilton_96_tiprack_1000uL_filter,
  cor_96_wellplate_360uL_Fb,
)


async def main():
  # 1. A simulated Hamilton STARlet: no robot needed, it just prints every command
  lh = LiquidHandler(backend=LiquidHandlerChatterboxBackend(), deck=STARLetDeck())
  await lh.setup()

  # 2. Put a tip carrier with one tip rack on the deck
  tip_car = TIP_CAR_480_A00(name="tip_carrier")
  tip_car[0] = hamilton_96_tiprack_1000uL_filter(name="tips")
  lh.deck.assign_child_resource(tip_car, rails=3)

  # 3. Put a plate carrier with one 96-well plate on the deck
  plt_car = PLT_CAR_L5AC_A00(name="plate_carrier")
  plt_car[0] = cor_96_wellplate_360uL_Fb(name="plate")
  lh.deck.assign_child_resource(plt_car, rails=15)

  # 4. Open the deck in your web browser (it opens by itself)
  vis = Visualizer(resource=lh)
  await vis.setup()
  await asyncio.sleep(3)  # time for the browser page to load

  tips = lh.deck.get_resource("tips")
  plate = lh.deck.get_resource("plate")

  # 5. The protocol: move 100 uL from well A1 to well A2
  await lh.pick_up_tips(tips["A1"])
  await asyncio.sleep(2)  # pause so you can watch
  await lh.aspirate(plate["A1"], vols=[100])
  await asyncio.sleep(2)  # pause so you can watch
  await lh.dispense(plate["A2"], vols=[100])
  await asyncio.sleep(2)  # pause so you can watch
  await lh.return_tips()
  await asyncio.sleep(2)  # pause so you can watch

  print("Protocol finished. Look at the browser, then press Enter to close.")
  input()
  await vis.stop()
  await lh.stop()


asyncio.run(main())