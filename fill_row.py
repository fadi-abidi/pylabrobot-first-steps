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
  lh = LiquidHandler(backend=LiquidHandlerChatterboxBackend(), deck=STARLetDeck())
  await lh.setup()

  tip_car = TIP_CAR_480_A00(name="tip_carrier")
  tip_car[0] = hamilton_96_tiprack_1000uL_filter(name="tips")
  lh.deck.assign_child_resource(tip_car, rails=3)

  plt_car = PLT_CAR_L5AC_A00(name="plate_carrier")
  plt_car[0] = cor_96_wellplate_360uL_Fb(name="plate")
  lh.deck.assign_child_resource(plt_car, rails=15)

  tips = lh.deck.get_resource("tips")
  plate = lh.deck.get_resource("plate")

  # Distribute 10 uL from well A1 to every other well of row A (A2 to A12)
  await lh.pick_up_tips(tips["A1"])
  for col in range(2, 13):
    await lh.aspirate(plate["A1"], vols=[10])
    await lh.dispense(plate[f"A{col}"], vols=[10])
  await lh.return_tips()

  await lh.stop()
  print("Row A filled")


asyncio.run(main())