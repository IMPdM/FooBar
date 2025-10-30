from db.queries.Sunstone.EOLAttachmentBody import EOLAttachmentBody

from algo.matej import matej

from utils.time import DateWindow
from utils.plants import Plants

from db.run_query import run_query
from db.connection import get_engine

engine = get_engine()

plant = Plants().get_plant("Sunstone_EOL_Att_Body")

params = {}
params.update(DateWindow.today())

all = run_query(engine, EOLAttachmentBody(plant), params)

matej(all)

# Tukaj potem kličeva alarmiranje v grafani

#zmenjeno