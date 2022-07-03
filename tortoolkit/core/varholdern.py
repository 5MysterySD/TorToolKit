# -*- coding: utf-8 -*-
# (c) YashDK [yash-dk@github]

from ..consts.ExecVarsSample import ExecVars
import os
import logging
import time

torlog = logging.getLogger(__name__)

class VarHolder:
    def __init__(self, var_db):
        self._var_dict = {}
        self._vardb = var_db

        sam1 = [68, 89, 78, 79]
        herstr = "".join(chr(i) for i in sam1)
        if os.environ.get(herstr,False):
            os.environ["TIME_STAT"] = str(time.time())

    def get_var(self, variable):
        if variable in self._var_dict.keys():
            torlog.debug("network call no made")
            return self._var_dict[variable]
        torlog.debug("Nework call made")
        db = self._vardb
        val = None

        #Get the variable from the constants supplied
        try:
            val = getattr(ExecVars,variable)
        except AttributeError:pass

        #Get the variable form the env [overlap]
        #try:
        envval = os.environ.get(variable)
        INTS = ["EDIT_SLEEP_SECS", "MAX_TORRENT_SIZE", "MAX_YTPLAYLIST_SIZE", "TG_UP_LIMIT", "API_ID", "STATUS_DEL_TOUT"]
        BOOLS = ["FORCE_DOCUMENTS", "LEECH_ENABLED", "RCLONE_ENABLED", "USETTINGS_IN_PRIVATE"]

        if variable == "ALD_USR":
            if envval is not None:
                templi = envval.split(" ")
                templi2 = []
                if len(templi) > 0:
                    for i in range(len(templi)):
                        try:
                            templi2.append(int(templi[i]))
                        except ValueError:
                            torlog.error(f"Invalid allow user {templi[i]} must be a integer.")
                if val is not None:
                    val.extend(templi2)
                else:
                    val = templi
        elif variable in INTS:
            val =  int(envval) if envval is not None else val
        elif variable in BOOLS:
            if envval:
                if not isinstance(val, bool):
                    val = "true" in envval.lower()
            else:
                val = None
        else:
            val =  envval if envval is not None else val

        #Get the variable form the DB [overlap]
        dbval, _ = db.get_variable(variable)

        if dbval is not None:
            val = dbval

        if val is None:
            torlog.error(
                f"The variable was not found in either the constants, environment or database. Variable is :- {variable}"
            )

                #raise Exception("The variable was not found in either the constants, environment or database. Variable is :- {}".format(variable))

        if isinstance(val,str):
            val = val.strip()

        self._var_dict[variable] = val
        return val

    def update_var(self, name, val):
        self._var_dict[name] = val 