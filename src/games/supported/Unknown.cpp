/* *****************************************************************************
 * A.L.E (Arcade Learning Environment)
 * Copyright (c) 2009-2013 by Yavar Naddaf, Joel Veness, Marc G. Bellemare and 
 *   the Reinforcement Learning and Artificial Intelligence Laboratory
 * Released under the GNU General Public License; see License.txt for details. 
 *
 * Based on: Stella  --  "An Atari 2600 VCS Emulator"
 * Copyright (c) 1995-2007 by Bradford W. Mott and the Stella team
 *
 * *****************************************************************************
 */
#include "Unknown.hpp"

#include "../RomUtils.hpp"
#include <iostream>

UnknownSettings::UnknownSettings() {
    reset();
}


/* create a new instance of the rom */
RomSettings* UnknownSettings::clone() const {
    
    RomSettings* rval = new UnknownSettings();
    *rval = *this;
    return rval;
}


/* process the latest information from ALE */
void UnknownSettings::step(const System& system) {

    // update the reward
    m_reward = 1;
    ++m_score;

    // update terminal status
    int lives = readRam(&system, 0xA1);
    m_terminal = lives == 0x0 || m_score > 999991;
}


/* is end of game */
bool UnknownSettings::isTerminal() const {

    return false; //m_terminal;
};


/* get the most recently observed reward */
reward_t UnknownSettings::getReward() const {
     return m_reward;
}


/* is an action part of the minimal set? */
bool UnknownSettings::isMinimal(const Action &a) const {
  return true;
}


/* reset the state of the game */
void UnknownSettings::reset() {
    
    m_reward   = 0;
    m_score    = 0;
    m_terminal = false;
}
        
/* saves the state of the rom settings */
void UnknownSettings::saveState(Serializer & ser) {
  ser.putInt(m_reward);
  ser.putInt(m_score);
  ser.putBool(m_terminal);
}

// loads the state of the rom settings
void UnknownSettings::loadState(Deserializer & ser) {
  m_reward = ser.getInt();
  m_score = ser.getInt();
  m_terminal = ser.getBool();
}

ActionVect UnknownSettings::getStartingActions() {
    ActionVect startingActions = getAllActions();
    return startingActions;
}
