import { StyleSheet, View } from 'react-native';

import { useTheme } from '@/hooks/use-theme';

export function ProgressBar({ progress }: { progress: number }) {
  const theme = useTheme();
  const clamped = Math.min(1, Math.max(0, progress));

  return (
    <View style={[styles.track, { backgroundColor: theme.backgroundElement }]}>
      <View
        style={[styles.fill, { backgroundColor: theme.accent, width: `${clamped * 100}%` }]}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  track: {
    height: 10,
    borderRadius: 5,
    overflow: 'hidden',
  },
  fill: {
    height: '100%',
    borderRadius: 5,
  },
});
