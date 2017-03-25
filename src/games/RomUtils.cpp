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
 *
 * RomUtils.hpp
 *
 * Additional utilities to operate on RAM.
 * *****************************************************************************
 */
#include "RomUtils.hpp"

#include "System.hxx"

/* reads a byte at a memory location between 0 and 128 */
int readRam(const System* system, int offset) {

	// peek modifies data-bus state, but is logically const from
	// the point of view of the RL interface
	System* sys = const_cast<System*>(system);

	return sys->peek((offset & 0x7F) + 0x80);
}

/* extracts a decimal value from a byte */
int getDecimalScore(int index, const System* system) {

	int score = 0;
	int digits_val = readRam(system, index);
	score = bcd_to_decimal(digits_val);
	return score;
}

/* turns a two-digit binary coded decimal into an int */
//TODO this only works with bytes, so technically we should use a byte-sized parameter
int bcd_to_decimal(int digits_val) {
	int right_digit = digits_val & 15;
	int left_digit = (digits_val - right_digit) >> 4;
	int score = (10 * left_digit) + right_digit;
	return score;
}

/* extracts a decimal value from 2 bytes */
int getDecimalScore(int lower_index, int higher_index, const System* system) {

	int score = getDecimalScore(lower_index, system);
	if (higher_index < 0) {
		return score;
	}
	score += 100 * getDecimalScore(higher_index, system);
	return score;
}

/* extracts a decimal value from 3 bytes */
int getDecimalScore(int lower_index, int middle_index, int higher_index,
		const System* system) {
	int score = getDecimalScore(lower_index, middle_index, system);
	if (higher_index < 0) {
		return score;
	}
	score += 10000 * getDecimalScore(higher_index, system);
	return score;
}

