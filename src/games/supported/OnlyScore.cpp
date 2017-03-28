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
#include "OnlyScore.hpp"

#include "../RomUtils.hpp"
#include <iostream>

OnlyScoreSettings::OnlyScoreSettings(int n, int low, int mid, int high) {
    this->m_n = n;
    this->m_low = low;
    this->m_mid = mid;
    this->m_high = high;
    reset();
}


/* create a new instance of the rom */
RomSettings* OnlyScoreSettings::clone() const {
    
    RomSettings* rval = new OnlyScoreSettings(m_n, m_low, m_mid, m_high);
    *rval = *this;
    return rval;
}


/* process the latest information from ALE */
void OnlyScoreSettings::step(const System& system) {
  reward_t score;
  if (m_n==3){
    score = getDecimalScore(m_low, m_mid, m_high, &system);
  } else if (m_n==2){
    score = getDecimalScore(m_low, m_mid, &system);
  }
      m_reward = score - m_score;
      m_score = score;
}


/* is end of game */
bool OnlyScoreSettings::isTerminal() const {
  //we don't know when it finishes
    return false;
};


/* get the most recently observed reward */
reward_t OnlyScoreSettings::getReward() const {
     return m_reward;
}


/* is an action part of the minimal set? */
bool OnlyScoreSettings::isMinimal(const Action &a) const {
  return true;
}


/* reset the state of the game */
void OnlyScoreSettings::reset() {
    
    m_reward   = 0;
    m_score    = 0;
    m_terminal = false;
}
        
/* saves the state of the rom settings */
void OnlyScoreSettings::saveState(Serializer & ser) {
  ser.putInt(m_reward);
  ser.putInt(m_score);
  ser.putBool(m_terminal);
}

// loads the state of the rom settings
void OnlyScoreSettings::loadState(Deserializer & ser) {
  m_reward = ser.getInt();
  m_score = ser.getInt();
  m_terminal = ser.getBool();
}

ActionVect OnlyScoreSettings::getStartingActions() {
    ActionVect startingActions = getAllActions();
    return startingActions;
}
