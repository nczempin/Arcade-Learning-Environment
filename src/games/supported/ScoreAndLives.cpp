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
#include "ScoreAndLives.hpp"

#include "../RomUtils.hpp"
#include <iostream>

ScoreAndLivesSettings::ScoreAndLivesSettings(int n, int low, int mid, int high,
    int lives) {
  this->m_n = n;
  this->m_low = low;
  this->m_mid = mid;
  this->m_high = high;
  this->m_lives_address = lives;
  reset();
}

/* create a new instance of the rom */
RomSettings* ScoreAndLivesSettings::clone() const {

  RomSettings* rval = new ScoreAndLivesSettings(m_n, m_low, m_mid, m_high, m_lives_address);
  *rval = *this;
  return rval;
}

/* process the latest information from ALE */
void ScoreAndLivesSettings::step(const System& system) {
  reward_t score = 0;
  if (m_n == 3) {
    score = getDecimalScore(m_low, m_mid, m_high, &system);
  } else if (m_n == 2) {
    score = getDecimalScore(m_low, m_mid, &system);
  }
  m_reward = score - m_score;
  m_score = score;
  m_lives = readRam(&system, m_lives_address);
  //TODO technically, it should be sufficient to update this in isTerminal()
  m_terminal = m_lives == 0;
}

/* is end of game */
bool ScoreAndLivesSettings::isTerminal() const {
  return m_terminal;
}
;

/* get the most recently observed reward */
reward_t ScoreAndLivesSettings::getReward() const {
  return m_reward;
}

/* is an action part of the minimal set? */
bool ScoreAndLivesSettings::isMinimal(const Action &a) const {
  return true;
}

/* reset the state of the game */
void ScoreAndLivesSettings::reset() {

  m_reward = 0;
  m_score = 0;
  m_terminal = false;
  m_lives = 3;
}

/* saves the state of the rom settings */
void ScoreAndLivesSettings::saveState(Serializer & ser) {
  ser.putInt(m_reward);
  ser.putInt(m_score);
  ser.putBool(m_terminal);
}

// loads the state of the rom settings
void ScoreAndLivesSettings::loadState(Deserializer & ser) {
  m_reward = ser.getInt();
  m_score = ser.getInt();
  m_terminal = ser.getBool();
}

ActionVect ScoreAndLivesSettings::getStartingActions() {
  ActionVect startingActions = getAllActions();
  return startingActions;
}
