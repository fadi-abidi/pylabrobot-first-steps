import asyncio

from pylabrobot.liquid_handling import LiquidHandler
from pylabrobot.liquid_handling.backends import LiquidHandlerChatterboxBackend
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

  tips = lh.deck.get_resource("tips")
  plate = lh.deck.get_resource("plate")

  # 4. The protocol: move 100 uL from well A1 to well A2
  await lh.pick_up_tips(tips["A1"])
  await lh.aspirate(plate["A1"], vols=[100])
  await lh.dispense(plate["A2"], vols=[100])
  await lh.return_tips()

  await lh.stop()
  print("Protocol finished")


asyncio.run(main())