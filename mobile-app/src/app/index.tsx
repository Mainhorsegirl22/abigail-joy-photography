import { useMemo, useState } from 'react';
import { Pressable, ScrollView, StyleSheet, TextInput, View } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';

import { ProgressBar } from '@/components/progress-bar';
import { ThemedText } from '@/components/themed-text';
import { ThemedView } from '@/components/themed-view';
import { MaxContentWidth, Spacing } from '@/constants/theme';
import { useTheme } from '@/hooks/use-theme';

type Expense = {
  id: string;
  name: string;
  amount: number;
};

const STARTER_EXPENSES: Expense[] = [
  { id: 'rent', name: 'Rent', amount: 1200 },
  { id: 'groceries', name: 'Groceries', amount: 350 },
  { id: 'utilities', name: 'Utilities', amount: 120 },
];

function toNumber(value: string) {
  const parsed = parseFloat(value.replace(/[^0-9.]/g, ''));
  return Number.isFinite(parsed) ? parsed : 0;
}

function formatCurrency(value: number) {
  return `$${value.toFixed(2)}`;
}

export default function BudgetPlannerScreen() {
  const theme = useTheme();

  const [income, setIncome] = useState('4000');
  const [expenses, setExpenses] = useState<Expense[]>(STARTER_EXPENSES);
  const [newExpenseName, setNewExpenseName] = useState('');
  const [newExpenseAmount, setNewExpenseAmount] = useState('');

  const [savingsGoal, setSavingsGoal] = useState('5000');
  const [currentSavings, setCurrentSavings] = useState('1200');

  const totalExpenses = useMemo(
    () => expenses.reduce((sum, expense) => sum + expense.amount, 0),
    [expenses],
  );
  const incomeValue = toNumber(income);
  const remaining = incomeValue - totalExpenses;

  const goalValue = toNumber(savingsGoal);
  const savedValue = toNumber(currentSavings);
  const goalProgress = goalValue > 0 ? savedValue / goalValue : 0;
  const amountLeftForGoal = Math.max(0, goalValue - savedValue);

  function addExpense() {
    const amount = toNumber(newExpenseAmount);
    if (!newExpenseName.trim() || amount <= 0) return;
    setExpenses((current) => [
      ...current,
      { id: `${Date.now()}`, name: newExpenseName.trim(), amount },
    ]);
    setNewExpenseName('');
    setNewExpenseAmount('');
  }

  function removeExpense(id: string) {
    setExpenses((current) => current.filter((expense) => expense.id !== id));
  }

  return (
    <ThemedView style={styles.screen}>
      <SafeAreaView style={styles.safeArea}>
        <ScrollView
          contentContainerStyle={styles.scrollContent}
          keyboardShouldPersistTaps="handled">
          <ThemedText type="title" style={styles.title}>
            Budget Planner
          </ThemedText>

          {/* Income */}
          <ThemedView type="backgroundElement" style={styles.card}>
            <ThemedText type="subtitle" style={styles.cardTitle}>
              Monthly income
            </ThemedText>
            <TextInput
              value={income}
              onChangeText={setIncome}
              keyboardType="decimal-pad"
              placeholder="0"
              placeholderTextColor={theme.textSecondary}
              style={[styles.incomeInput, { color: theme.text }]}
            />
          </ThemedView>

          {/* Expenses */}
          <ThemedView type="backgroundElement" style={styles.card}>
            <ThemedText type="subtitle" style={styles.cardTitle}>
              Expenses
            </ThemedText>

            {expenses.map((expense) => (
              <View key={expense.id} style={styles.row}>
                <ThemedText style={styles.rowLabel}>{expense.name}</ThemedText>
                <ThemedText type="smallBold">{formatCurrency(expense.amount)}</ThemedText>
                <Pressable
                  onPress={() => removeExpense(expense.id)}
                  hitSlop={8}
                  style={({ pressed }) => [styles.removeButton, pressed && styles.pressed]}>
                  <ThemedText themeColor="negative" type="smallBold">
                    Remove
                  </ThemedText>
                </Pressable>
              </View>
            ))}

            <View style={styles.addExpenseRow}>
              <TextInput
                value={newExpenseName}
                onChangeText={setNewExpenseName}
                placeholder="Expense name"
                placeholderTextColor={theme.textSecondary}
                style={[styles.addExpenseNameInput, { color: theme.text }]}
              />
              <TextInput
                value={newExpenseAmount}
                onChangeText={setNewExpenseAmount}
                keyboardType="decimal-pad"
                placeholder="Amount"
                placeholderTextColor={theme.textSecondary}
                style={[styles.addExpenseAmountInput, { color: theme.text }]}
              />
              <Pressable
                onPress={addExpense}
                style={({ pressed }) => [
                  styles.addButton,
                  { backgroundColor: theme.accent },
                  pressed && styles.pressed,
                ]}>
                <ThemedText style={styles.addButtonLabel} type="smallBold">
                  Add
                </ThemedText>
              </Pressable>
            </View>
          </ThemedView>

          {/* Summary */}
          <ThemedView type="backgroundElement" style={styles.card}>
            <ThemedText type="subtitle" style={styles.cardTitle}>
              Summary
            </ThemedText>
            <View style={styles.row}>
              <ThemedText style={styles.rowLabel}>Income</ThemedText>
              <ThemedText type="smallBold">{formatCurrency(incomeValue)}</ThemedText>
            </View>
            <View style={styles.row}>
              <ThemedText style={styles.rowLabel}>Total expenses</ThemedText>
              <ThemedText type="smallBold">{formatCurrency(totalExpenses)}</ThemedText>
            </View>
            <View style={styles.row}>
              <ThemedText style={styles.rowLabel}>Remaining</ThemedText>
              <ThemedText themeColor={remaining >= 0 ? 'positive' : 'negative'} type="smallBold">
                {formatCurrency(remaining)}
              </ThemedText>
            </View>
          </ThemedView>

          {/* Savings goal */}
          <ThemedView type="backgroundElement" style={styles.card}>
            <ThemedText type="subtitle" style={styles.cardTitle}>
              Savings goal
            </ThemedText>

            <View style={styles.goalInputsRow}>
              <View style={styles.goalInputGroup}>
                <ThemedText type="small" themeColor="textSecondary">
                  Goal
                </ThemedText>
                <TextInput
                  value={savingsGoal}
                  onChangeText={setSavingsGoal}
                  keyboardType="decimal-pad"
                  style={[styles.goalInput, { color: theme.text }]}
                />
              </View>
              <View style={styles.goalInputGroup}>
                <ThemedText type="small" themeColor="textSecondary">
                  Saved so far
                </ThemedText>
                <TextInput
                  value={currentSavings}
                  onChangeText={setCurrentSavings}
                  keyboardType="decimal-pad"
                  style={[styles.goalInput, { color: theme.text }]}
                />
              </View>
            </View>

            <ProgressBar progress={goalProgress} />

            <View style={styles.goalFooterRow}>
              <ThemedText type="small" themeColor="textSecondary">
                {Math.round(goalProgress * 100)}% of goal
              </ThemedText>
              <ThemedText type="small" themeColor="textSecondary">
                {formatCurrency(amountLeftForGoal)} to go
              </ThemedText>
            </View>
          </ThemedView>
        </ScrollView>
      </SafeAreaView>
    </ThemedView>
  );
}

const styles = StyleSheet.create({
  screen: {
    flex: 1,
  },
  safeArea: {
    flex: 1,
    alignItems: 'center',
  },
  scrollContent: {
    width: '100%',
    maxWidth: MaxContentWidth,
    paddingHorizontal: Spacing.four,
    paddingTop: Spacing.four,
    paddingBottom: Spacing.six,
    gap: Spacing.four,
  },
  title: {
    marginBottom: Spacing.two,
  },
  card: {
    borderRadius: Spacing.three,
    padding: Spacing.four,
    gap: Spacing.three,
  },
  cardTitle: {
    fontSize: 18,
    lineHeight: 24,
  },
  row: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: Spacing.two,
  },
  rowLabel: {
    flex: 1,
  },
  removeButton: {
    paddingHorizontal: Spacing.one,
    paddingVertical: Spacing.half,
  },
  pressed: {
    opacity: 0.7,
  },
  incomeInput: {
    fontSize: 32,
    fontWeight: '600',
    paddingVertical: Spacing.one,
  },
  addExpenseRow: {
    flexDirection: 'row',
    gap: Spacing.two,
    marginTop: Spacing.one,
  },
  addExpenseNameInput: {
    flex: 2,
    borderBottomWidth: 1,
    borderBottomColor: 'rgba(128,128,128,0.4)',
    paddingVertical: Spacing.one,
  },
  addExpenseAmountInput: {
    flex: 1,
    borderBottomWidth: 1,
    borderBottomColor: 'rgba(128,128,128,0.4)',
    paddingVertical: Spacing.one,
  },
  addButton: {
    borderRadius: Spacing.two,
    paddingHorizontal: Spacing.three,
    justifyContent: 'center',
    alignItems: 'center',
  },
  addButtonLabel: {
    color: '#ffffff',
  },
  goalInputsRow: {
    flexDirection: 'row',
    gap: Spacing.three,
  },
  goalInputGroup: {
    flex: 1,
    gap: Spacing.half,
  },
  goalInput: {
    fontSize: 20,
    fontWeight: '600',
    borderBottomWidth: 1,
    borderBottomColor: 'rgba(128,128,128,0.4)',
    paddingVertical: Spacing.one,
  },
  goalFooterRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
});
